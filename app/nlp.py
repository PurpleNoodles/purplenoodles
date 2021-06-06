from google.cloud import language_v1
from datetime import date

client = language_v1.LanguageServiceClient()

def generate_report(text: str, user_info):
    document = language_v1.Document(
        content = text,
        type_ = 'PLAIN_TEXT',
        language = 'en'
    )

    sentiment_response = client.analyze_sentiment(
        document = document,
        encoding_type = 'UTF32'
    )

    entity_sentiment_response = client.analyze_entity_sentiment(
        document = document,
        encoding_type = 'UTF32'
    )

    current_date = date.today().strftime("%d %B %Y")

    severity = round(sentiment_response.document_sentiment.score*10)

    likely_offenders = []
    for entity in entity_sentiment_response.entities:
        if entity.type_ == 1 and entity.sentiment.score < 0:
            likely_offenders.append(entity)
    likely_offender = sorted(likely_offenders, key=lambda offender: offender.sentiment.score)[0]

    split_offender_name = likely_offender.name.split(' ')
    offender_mentions = ""
    for sentence in sentiment_response.sentences:
        if split_offender_name[0] in sentence.text.content or split_offender_name[1] in sentence.text.content:
            offender_mentions += "<li>{}</li>".format(sentence.text.content)

    relational_offense = []
    for entity in entity_sentiment_response.entities:
        if entity.type_ == 7 and entity.sentiment.score < 0:
            relational_offense.append(entity)
    related_offense = sorted(relational_offense, key=lambda relation: relation.sentiment.score)[0]

    related_mentions = ""
    for sentence in sentiment_response.sentences:
        if related_offense.name in sentence.text.content:
            related_mentions += "<li>{}</li>".format(sentence.text.content)

    significant_sentences = ""
    for sentence in sentiment_response.sentences:
        if sentence.sentiment.score <= -0.75:
            significant_sentences += "<ul><li><p>{}</p></li></ul>".format(sentence.text.content)

    possible_people = []
    for entity in entity_sentiment_response.entities:
        if entity.type_ == 1 and entity != likely_offender:
            possible_people.append(entity)
    possible_people_bullets = "<ul>"
    for person in possible_people:
        possible_people_bullets += "\n<li>{}</li>".format(person.name)
    possible_people_bullets += "\n</ul>"

    rep = """
    <h1>{0} - {1} </h1>

    <h2>{2} | Severity: {3} </h2>

    <p>{4} may be the offender regarding this matter. Look through these instances of said name for more detail:

    <ul>{5}</ul></p>

    <p>Note that the {6} can be related to this offense. View the following statement(s):

    <ul>{7}</ul></p>

    <h2>Here we would like to provide you with the most significant portions of this offense.</h2>

    {8}

    <h4>Other people possibly involved:</h4>
    {9}

    <h1>View the original submission below.</h1>
    <pre><code>
    {10}
    </pre></code>

    <h4>Please contact info@purplenoodles.co if you have suggestions on how our reports can be improved. Thank you.</h4>
    """.format(
        (user_info['firstname'] + ' ' + user_info['lastname']),
        user_info['email'],
        current_date,
        severity,
        likely_offender.name,
        offender_mentions,
        related_offense.name,
        related_mentions,
        significant_sentences,
        possible_people_bullets,
        text
    )

    return {
        'organization_id': user_info['organization_id'],
        'user_id': user_info['user_id'],
        'severity': severity,
        'report': rep
    }