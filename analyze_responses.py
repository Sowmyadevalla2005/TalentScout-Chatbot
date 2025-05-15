import os
import json
from typing import Dict, List
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from utils import calculate_response_quality

def load_candidate_responses(directory: str = "candidate_responses") -> List[Dict]:
    """Load all candidate response files from the directory."""
    responses = []
    if not os.path.exists(directory):
        print(f"No responses directory found at {directory}")
        return responses
        
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                        response_data = json.load(f)
                        responses.append(response_data)
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
                    continue
    except Exception as e:
        print(f"Error accessing directory: {str(e)}")
    
    print(f"Loaded {len(responses)} candidate responses")
    return responses

def analyze_technical_proficiency(responses: List[Dict]) -> pd.DataFrame:
    """Analyze technical proficiency based on response quality."""
    proficiency_data = []
    
    for response in responses:
        candidate_name = response["personal_info"]["name"]
        tech_assessment = response["technical_assessment"]
        
        # Calculate average metrics
        quality_metrics = tech_assessment.get("quality_metrics", [])
        if quality_metrics:
            avg_word_count = sum(m["word_count"] for m in quality_metrics) / len(quality_metrics)
            technical_terms_ratio = sum(1 for m in quality_metrics if m["has_technical_terms"]) / len(quality_metrics)
            detailed_ratio = sum(1 for m in quality_metrics if m["is_detailed"]) / len(quality_metrics)
            examples_ratio = sum(1 for m in quality_metrics if m["has_examples"]) / len(quality_metrics)
            
            proficiency_data.append({
                "candidate_name": candidate_name,
                "avg_response_length": avg_word_count,
                "technical_term_usage": technical_terms_ratio * 100,
                "detailed_responses": detailed_ratio * 100,
                "example_usage": examples_ratio * 100,
                "tech_stack_size": len(response["personal_info"]["tech_stack"]),
                "experience_years": float(response["personal_info"]["experience"].split()[0]) if response["personal_info"]["experience"] else 0
            })
    
    return pd.DataFrame(proficiency_data)

def analyze_sentiment_trends(responses: List[Dict]) -> pd.DataFrame:
    """Analyze sentiment trends across all candidates."""
    sentiment_data = []
    
    for response in responses:
        candidate_name = response["personal_info"]["name"]
        sentiments = response["technical_assessment"]["sentiment_history"]
        
        if sentiments:
            total = len(sentiments)
            sentiment_data.append({
                "candidate_name": candidate_name,
                "positive_ratio": (sentiments.count("positive") / total) * 100,
                "negative_ratio": (sentiments.count("negative") / total) * 100,
                "neutral_ratio": (sentiments.count("neutral") / total) * 100,
                "total_responses": total,
                "interview_duration": response.get("interview_duration", 0),
                "completion_status": response.get("completion_status", "unknown")
            })
    
    return pd.DataFrame(sentiment_data)

def analyze_tech_stack_trends(responses: List[Dict]) -> pd.DataFrame:
    """Analyze common technologies and experience levels."""
    tech_data = []
    
    for response in responses:
        for tech in response["personal_info"]["tech_stack"]:
            tech_data.append({
                "technology": tech.lower().strip(),
                "experience_level": response.get("personal_info", {}).get("experience", "unknown"),
                "position": response.get("personal_info", {}).get("position", "unknown")
            })
    
    return pd.DataFrame(tech_data)

def generate_visualizations(prof_df: pd.DataFrame, sent_df: pd.DataFrame, tech_df: pd.DataFrame, output_dir: str = "analysis_reports"):
    """Generate visualization plots for the analysis."""
    os.makedirs(output_dir, exist_ok=True)
    plt.style.use('seaborn')
    
    # Technical Proficiency Plot
    plt.figure(figsize=(12, 6))
    prof_metrics = prof_df[["avg_response_length", "technical_term_usage", "detailed_responses", "example_usage"]].mean()
    prof_metrics.plot(kind='bar')
    plt.title("Average Technical Proficiency Metrics")
    plt.ylabel("Percentage / Score")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "technical_proficiency.png"))
    plt.close()
    
    # Sentiment Distribution
    plt.figure(figsize=(10, 6))
    sent_avg = sent_df[["positive_ratio", "neutral_ratio", "negative_ratio"]].mean()
    sent_avg.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Overall Sentiment Distribution")
    plt.savefig(os.path.join(output_dir, "sentiment_distribution.png"))
    plt.close()
    
    # Technology Trends
    if not tech_df.empty:
        plt.figure(figsize=(12, 6))
        tech_counts = tech_df["technology"].value_counts().head(10)
        tech_counts.plot(kind='bar')
        plt.title("Top 10 Technologies Mentioned")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "technology_trends.png"))
        plt.close()

def generate_report(directory: str = "candidate_responses") -> None:
    """Generate a comprehensive analysis report."""
    # Load responses
    responses = load_candidate_responses(directory)
    if not responses:
        print("No candidate responses found.")
        return
    
    # Perform analysis
    prof_df = analyze_technical_proficiency(responses)
    sent_df = analyze_sentiment_trends(responses)
    tech_df = analyze_tech_stack_trends(responses)
    
    # Generate visualizations
    generate_visualizations(prof_df, sent_df, tech_df)
    
    # Generate report
    report = f"""
    TalentScout Technical Screening Analysis Report
    Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    1. Overview
    --------------------
    Total Candidates: {len(responses)}
    Completed Interviews: {sum(1 for r in responses if r.get('completion_status') == 'completed')}
    Average Interview Duration: {sent_df['interview_duration'].mean():.1f} interactions
    
    2. Technical Proficiency
    -----------------------
    Average Response Length: {prof_df['avg_response_length'].mean():.1f} words
    Technical Term Usage: {prof_df['technical_term_usage'].mean():.1f}%
    Detailed Responses: {prof_df['detailed_responses'].mean():.1f}%
    Example Usage: {prof_df['example_usage'].mean():.1f}%
    
    3. Technology Trends
    -------------------
    Most Common Technologies:
    {tech_df['technology'].value_counts().head(5).to_string()}
    
    4. Sentiment Analysis
    --------------------
    Average Sentiment Distribution:
    - Positive Responses: {sent_df['positive_ratio'].mean():.1f}%
    - Neutral Responses: {sent_df['neutral_ratio'].mean():.1f}%
    - Negative Responses: {sent_df['negative_ratio'].mean():.1f}%
    
    5. Candidate Performance Summary
    ------------------------------
    {prof_df.sort_values('avg_response_length', ascending=False)[['candidate_name', 'avg_response_length', 'technical_term_usage']].head().to_string()}
    
    Note: Visualizations have been saved in the analysis_reports directory.
    """
    
    # Save report
    report_file = f"analysis_reports/screening_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    os.makedirs("analysis_reports", exist_ok=True)
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Analysis report generated: {report_file}")
    print("Visualizations saved in analysis_reports directory")

if __name__ == "__main__":
    generate_report() 