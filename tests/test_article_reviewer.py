"""
Test suite for article_reviewer.py
"""

import unittest
import json
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile

# Add parent directories and app directory to path for imports
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))
sys.path.insert(0, str(root_path / "app" / "ArticleReviewer"))

from article_reviewer import (
    DeleteModel,
    ModifyModel,
    InsertModel,
    ArticleReviewModel,
    ArticleReviewer
)
from article_reviewer_cli import cli
from article_reviewer_prompts import PromptBuilder
from lite.config import ModelConfig


class TestModels(unittest.TestCase):
    """Test Pydantic models for article review"""

    def test_delete_model_valid(self):
        """Test DeleteModel with valid data"""
        delete = DeleteModel(
            line_number=5,
            content="unnecessary phrase",
            reason="This phrase is redundant",
            severity="medium"
        )
        self.assertEqual(delete.line_number, 5)
        self.assertEqual(delete.severity, "medium")

    def test_modify_model_valid(self):
        """Test ModifyModel with valid data"""
        modify = ModifyModel(
            line_number=10,
            original_content="The data is showed",
            suggested_modification="The data is shown",
            reason="Grammar correction",
            severity="high"
        )
        self.assertEqual(modify.line_number, 10)
        self.assertEqual(modify.severity, "high")

    def test_insert_model_valid(self):
        """Test InsertModel with valid data"""
        insert = InsertModel(
            line_number=15,
            suggested_content="Additional context here",
            reason="Missing explanation",
            section="Introduction",
            severity="low"
        )
        self.assertEqual(insert.section, "Introduction")
        self.assertEqual(insert.severity, "low")

    def test_article_review_model_valid(self):
        """Test ArticleReviewModel with valid data"""
        response = ArticleReviewModel(
            score=85,
            total_issues=3,
            summary="Well-written article with minor issues",
            deletions=[],
            modifications=[],
            insertions=[],
            proofreading_rules_applied=["Grammar"]
        )
        self.assertEqual(response.score, 85)
        self.assertEqual(response.total_issues, 3)

    def test_article_review_model_with_issues(self):
        """Test ArticleReviewModel with all issue types"""
        delete = DeleteModel(
            line_number=1,
            content="redundant",
            reason="Redundant text",
            severity="low"
        )
        modify = ModifyModel(
            line_number=2,
            original_content="original",
            suggested_modification="modified",
            reason="Improve clarity",
            severity="medium"
        )
        insert = InsertModel(
            line_number=3,
            suggested_content="new content",
            reason="Add missing info",
            section="Conclusion",
            severity="high"
        )
        
        response = ArticleReviewModel(
            score=85,
            total_issues=3,
            summary="Review with issues",
            deletions=[delete],
            modifications=[modify],
            insertions=[insert],
            proofreading_rules_applied=["Rule 1"]
        )
        self.assertEqual(len(response.deletions), 1)
        self.assertEqual(len(response.modifications), 1)
        self.assertEqual(len(response.insertions), 1)

        response = ArticleReviewModel(
            score=72,
            total_issues=3,
            summary="Multiple issues to address",
            deletions=[delete],
            modifications=[modify],
            insertions=[insert],
            proofreading_rules_applied=["Content"]
        )
        self.assertEqual(len(response.deletions), 1)
        self.assertEqual(len(response.modifications), 1)
        self.assertEqual(len(response.insertions), 1)
        self.assertEqual(response.total_issues, 3)


class TestCLI(unittest.TestCase):
    """Test CLI functionality"""

    @patch('article_reviewer.LiteClient')
    def test_cli_with_simple_text(self, mock_client_class):
        """Test CLI with simple article text"""
        # Create mock response
        mock_response = {
            "score": 90,
            "total_issues": 1,
            "summary": "Excellent article",
            "deletions": [],
            "modifications": [
                {
                    "line_number": 1,
                    "original_content": "Test",
                    "suggested_modification": "Testing",
                    "reason": "Better phrasing",
                    "severity": "low"
                }
            ],
            "insertions": [],
            "proofreading_rules_applied": ["Grammar"]
        }

        mock_instance = MagicMock()
        mock_instance.generate_text.return_value = json.dumps(mock_response)
        mock_client_class.return_value = mock_instance

        # Test with simple text
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                article = "This is a test article for reviewing."
                cli(article)

                # Verify client was called
                mock_client_class.assert_called_once()
                mock_instance.generate_text.assert_called_once()
            finally:
                os.chdir(original_cwd)

    @patch('article_reviewer.LiteClient')
    def test_cli_with_custom_model(self, mock_client_class):
        """Test CLI with custom model specification"""
        mock_response = {
            "score": 85,
            "total_issues": 0,
            "summary": "Good article",
            "deletions": [],
            "modifications": [],
            "insertions": [],
            "proofreading_rules_applied": []
        }

        mock_instance = MagicMock()
        mock_instance.generate_text.return_value = json.dumps(mock_response)
        mock_client_class.return_value = mock_instance

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                article = "Test article"
                cli(article, model_name="gpt-4")

                # Verify correct model was specified
                call_args = mock_client_class.call_args
                self.assertEqual(call_args[1]['model_config'].model, "gpt-4")
            finally:
                os.chdir(original_cwd)

    @patch('article_reviewer.LiteClient')
    def test_cli_output_file_creation(self, mock_client_class):
        """Test that CLI creates output JSON file"""
        mock_response = {
            "score": 75,
            "total_issues": 1,
            "summary": "Needs improvement",
            "deletions": [
                {
                    "line_number": 5,
                    "content": "redundant",
                    "reason": "Unnecessary",
                    "severity": "low"
                }
            ],
            "modifications": [],
            "insertions": [],
            "proofreading_rules_applied": []
        }

        mock_instance = MagicMock()
        mock_instance.generate_text.return_value = json.dumps(mock_response)
        mock_client_class.return_value = mock_instance

        # Important: the current implementation saves to "outputs" directory by default
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                article = "Test article for output"
                cli(article)

                # Check that output file was created in "outputs" directory
                output_dir = os.path.join(tmpdir, "outputs")
                self.assertTrue(os.path.exists(output_dir))
                output_files = [f for f in os.listdir(output_dir) if f.startswith('article_review_')]
                self.assertEqual(len(output_files), 1)

                # Verify file contents
                with open(os.path.join(output_dir, output_files[0]), 'r') as f:
                    saved_data = json.load(f)
                    self.assertEqual(saved_data['score'], 75)
                    self.assertEqual(saved_data['total_issues'], 1)
            finally:
                os.chdir(original_cwd)


class TestValidation(unittest.TestCase):
    """Test input validation"""

    def test_severity_levels(self):
        """Test that severity levels are properly handled"""
        severities = ["low", "medium", "high", "critical"]

        for severity in severities:
            delete = DeleteModel(
                line_number=1,
                content="test",
                reason="test",
                severity=severity
            )
            self.assertEqual(delete.severity, severity)

    def test_line_number_required(self):
        """Test that line_number is required"""
        from pydantic import ValidationError
        with self.assertRaises(ValidationError):
            DeleteModel(
                content="test",
                reason="test",
                severity="low"
            )

    def test_content_required(self):
        """Test that content is required"""
        from pydantic import ValidationError
        with self.assertRaises(ValidationError):
            DeleteModel(
                line_number=1,
                reason="test",
                severity="low"
            )


class TestArticleReviewer(unittest.TestCase):
    """Test ArticleReviewer class"""

    @patch('article_reviewer.LiteClient')
    def test_reviewer_initialization(self, mock_client_class):
        """Test ArticleReviewer initialization"""
        model_config = ModelConfig(model="gpt-4")
        reviewer = ArticleReviewer(model_config=model_config)
        self.assertEqual(reviewer.model_name, "gpt-4")
        self.assertIsNotNone(reviewer.client)

    @patch('article_reviewer.LiteClient')
    def test_reviewer_default_model(self, mock_client_class):
        """Test ArticleReviewer with default model"""
        reviewer = ArticleReviewer()
        self.assertEqual(reviewer.model_name, "ollama/gemma3")

    @patch('article_reviewer.LiteClient')
    def test_review_method(self, mock_client_class):
        """Test review method returns ArticleReviewModel"""
        mock_response = {
            "score": 85,
            "total_issues": 1,
            "summary": "Good article",
            "deletions": [],
            "modifications": [
                {
                    "line_number": 1,
                    "original_content": "test",
                    "suggested_modification": "tested",
                    "reason": "Grammar",
                    "severity": "low"
                }
            ],
            "insertions": [],
            "proofreading_rules_applied": ["Grammar"]
        }

        mock_instance = MagicMock()
        mock_instance.generate_text.return_value = json.dumps(mock_response)
        mock_client_class.return_value = mock_instance

        reviewer = ArticleReviewer()
        result = reviewer.review("Test article")

        self.assertIsInstance(result, ArticleReviewModel)
        self.assertEqual(result.score, 85)
        self.assertEqual(result.total_issues, 1)
        self.assertEqual(len(result.modifications), 1)

    @patch('article_reviewer.LiteClient')
    def test_save_review_with_default_filename(self, mock_client_class):
        """Test save_review generates timestamped filename"""
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance

        reviewer = ArticleReviewer()
        review = ArticleReviewModel(
            score=80,
            total_issues=0,
            summary="Good",
            deletions=[],
            modifications=[],
            insertions=[],
            proofreading_rules_applied=[]
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                # By default it saves to 'outputs' subdirectory
                filename = reviewer.save_review(review, output_dir=tmpdir)

                # Check filename follows pattern
                self.assertTrue(os.path.basename(filename).startswith("article_review_"))
                self.assertTrue(filename.endswith(".json"))

                # Check file was created
                self.assertTrue(os.path.exists(filename))

                # Check file contents
                with open(filename, 'r') as f:
                    data = json.load(f)
                    self.assertEqual(data['score'], 80)
            finally:
                os.chdir(original_cwd)

    @patch('article_reviewer.LiteClient')
    def test_save_review_with_custom_filename(self, mock_client_class):
        """Test save_review with custom filename"""
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance

        reviewer = ArticleReviewer()
        review = ArticleReviewModel(
            score=75,
            total_issues=2,
            summary="Fair",
            deletions=[],
            modifications=[],
            insertions=[],
            proofreading_rules_applied=[]
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)
            try:
                custom_filename = "my_review.json"
                # reviewer.save_review appends _review.json if it doesn't end with it, 
                # and places it in output_dir
                filename = reviewer.save_review(review, output_filename=custom_filename, output_dir=tmpdir)

                self.assertTrue(filename.endswith("my_review.json"))
                self.assertTrue(os.path.exists(filename))

                # Check file contents
                with open(filename, 'r') as f:
                    data = json.load(f)
                    self.assertEqual(data['score'], 75)
                    self.assertEqual(data['total_issues'], 2)
            finally:
                os.chdir(original_cwd)

    @patch('article_reviewer.LiteClient')
    def test_print_review_output(self, mock_client_class):
        """Test print_review produces output"""
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance

        reviewer = ArticleReviewer()
        review = ArticleReviewModel(
            score=90,
            total_issues=0,
            summary="Excellent",
            deletions=[],
            modifications=[],
            insertions=[],
            proofreading_rules_applied=[]
        )

        # Capture print output
        from io import StringIO
        import sys as sys_module

        captured_output = StringIO()
        sys_module.stdout = captured_output
        reviewer.print_review(review)
        sys_module.stdout = sys_module.__stdout__

        output = captured_output.getvalue()
        self.assertIn("ARTICLE REVIEW REPORT", output)
        self.assertIn("Overall Score: 90/100", output)
        self.assertIn("Excellent", output)

    def test_proofreading_rules_constant(self):
        """Test PROOFREADING_RULES is properly defined in PromptBuilder"""
        self.assertIn("Grammar & Syntax", PromptBuilder.PROOFREADING_RULES)
        self.assertIn("Style & Clarity", PromptBuilder.PROOFREADING_RULES)
        self.assertIn("Formatting & Punctuation", PromptBuilder.PROOFREADING_RULES)
        self.assertIn("Content & Structure", PromptBuilder.PROOFREADING_RULES)
        self.assertIn("Consistency", PromptBuilder.PROOFREADING_RULES)


if __name__ == "__main__":
    unittest.main()
