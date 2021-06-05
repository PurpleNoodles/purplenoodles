from google.cloud import language_v1

client = language_v1.LanguageServiceClient()

document = language_v1.Document(
    content='Jogging is not very fun',
    type_='PLAIN_TEXT',
    language='en'
)

response = client.analyze_sentiment(
    document=document,
    encoding_type='UTF32'
)

print("Document sentiment score: {}".format(response.document_sentiment.score))
print("Document sentiment magnitude: {}".format(response.document_sentiment.magnitude))