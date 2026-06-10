from scam_detector import analyze_text


def test_analyze_text():
    sample = "Congratulations! You have won a prize. Click the link to claim it and send your bank details."
    result = analyze_text(sample)
    assert isinstance(result, dict)
    assert "risk_score" in result
    assert "threat_level" in result
    assert "reasons" in result
    assert "recommendations" in result


if __name__ == "__main__":
    test_analyze_text()
    print("test_analyze_text passed")
