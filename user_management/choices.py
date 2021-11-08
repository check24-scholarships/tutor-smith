# Choices for models, sites, etc
# Use (id, human readable name) the id will be saved in the db
# TODO: Add subjects
choice_subject = (
    (0, 'Deutsch'),
    (1, 'Mathe'),
    (2, 'Englisch'),
    (3, 'Chemie'),
    (4, 'Informatik'),
)
choice_difficulty = [(0, 'Beginner'), (1, 'Medium'), (2, 'Hard')]

choice_gender = [
    (9, 'Not Stated'),
    (1, 'Männlich'),
    (2, 'Weiblich'),
    (3, 'Another Term'),
]

choice_ticket_type = [
    (1, 'Report'),
    (2, 'Bug'),
    (3, 'Request'),
]

choice_ticket_status = [
    (1, 'Rejected'),
    (2, 'Review Pending'),
    (3, 'Reviewing'),
    (4, 'Finished'),
]
