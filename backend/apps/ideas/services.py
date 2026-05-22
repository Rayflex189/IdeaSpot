
# Business logic helpers
def can_generate_prd(idea):
    return idea.status == Idea.Status.DRAFT
