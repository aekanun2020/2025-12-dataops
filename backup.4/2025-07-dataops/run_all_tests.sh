#!/bin/bash
# Script สำหรับรัน tests ในเครื่อง local

echo "🧪 Running Unit Tests for Loan ETL Pipeline..."
echo "============================================"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
echo "📊 Running tests with coverage..."
pytest tests/ -v --cov=pre-production/etl --cov-report=term-missing --cov-report=html

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo "📈 Coverage report saved to: htmlcov/index.html"
else
    echo ""
    echo "❌ Some tests failed!"
    exit 1
fi

echo ""
echo "✨ Testing completed!"
