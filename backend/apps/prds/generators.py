from utils.constants import PRD_SECTION_TEMPLATE

def generate_prd_content(idea):
    """Generate structured PRD content from an idea."""
    content = PRD_SECTION_TEMPLATE.copy()
    # Customize sections with idea data
    content['sections'][0]['body'] = idea.raw_description[:500]  # Overview
    content['sections'][1]['body'] = f"Problem: {idea.title}\n\n{idea.scanty_note}"
    content['sections'][2]['body'] = "Define clear success criteria."
    return content
