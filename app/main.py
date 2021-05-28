from rdflib_endpoint import SparqlEndpoint

import rdflib
# from rdflib.plugins.sparql.evaluate import evalPart, evalBGP
from rdflib.plugins.sparql.evalutils import _eval
from rdflib import Graph, Literal, RDF, URIRef
# from rdflib.namespace import Namespace

from openpredict.openpredict_model import query_omim_drugbank_classifier
from openpredict.openpredict_utils import init_openpredict_dir

def most_similar(query_results, ctx, part, eval_part):
    """
    Get most similar entities for a given entity

    Query:
    PREFIX openpredict: <https://w3id.org/um/openpredict/>
    SELECT ?drugOrDisease ?mostSimilar ?mostSimilarScore WHERE {
        BIND("OMIM:246300" AS ?drugOrDisease)
        BIND(openpredict:most_similar(?drugOrDisease) AS ?mostSimilar)
    """
    argumentEntity = str(_eval(part.expr.expr[0], eval_part.forget(ctx, _except=part.expr._vars)))
    try:
        argumentLimit = str(_eval(part.expr.expr[1], eval_part.forget(ctx, _except=part.expr._vars)))
    except:
        argumentLimit = None
    
    # TODO: get similarity from dataframe using argumentEntity
    # Using stub data
    similarity_results = [{'mostSimilar': 'DRUGBANK:DB00001', 'score': 0.42}]
    
    evaluation = []
    scores = []
    for most_similar in similarity_results:
        evaluation.append(most_similar['mostSimilar'])
        scores.append(most_similar['score'])

    # Append the results for our custom function
    for i, result in enumerate(evaluation):
        query_results.append(eval_part.merge({
            part.var: Literal(result), 
            rdflib.term.Variable(part.var + 'Score'): Literal(scores[i])
        }))
    return query_results, ctx, part, eval_part


def get_predictions(query_results, ctx, part, eval_part):
    """
    Query OpenPredict classifier to get drug/disease predictions

    Query:
    PREFIX openpredict: <https://w3id.org/um/openpredict/>
    SELECT ?drugOrDisease ?predictedForTreatment ?predictedForTreatmentScore WHERE {
        BIND("OMIM:246300" AS ?drugOrDisease)
        BIND(openpredict:prediction(?drugOrDisease) AS ?predictedForTreatment)
    """
    argument1 = str(_eval(part.expr.expr[0], eval_part.forget(ctx, _except=part.expr._vars)))

    # Run the classifier to get predictions and scores for the entity given as argument
    predictions_list = query_omim_drugbank_classifier(argument1, 'openpredict-baseline-omim-drugbank')

    evaluation = []
    scores = []
    for prediction in predictions_list:
        # Quick fix to get results for drugs or diseases
        if argument1.startswith('OMIM') or argument1.startswith('MONDO'):
            evaluation.append(prediction['drug'])
        else:
            evaluation.append(prediction['disease'])
        scores.append(prediction['score'])
    # Append the results for our custom function
    for i, result in enumerate(evaluation):
        query_results.append(eval_part.merge({
            part.var: Literal(result), 
            rdflib.term.Variable(part.var + 'Score'): Literal(scores[i])
        }))
    return query_results, ctx, part, eval_part


example_query = """Example query:\n
```
PREFIX openpredict: <https://w3id.org/um/openpredict/>
SELECT ?drugOrDisease ?predictedForTreatment ?predictedForTreatmentScore WHERE {
    BIND("OMIM:246300" AS ?drugOrDisease)
    BIND(openpredict:prediction(?drugOrDisease) AS ?predictedForTreatment)
}
```"""

init_openpredict_dir()
# Start the SPARQL endpoint based on a RDFLib Graph
g = Graph()
app = SparqlEndpoint(
    graph=g,
    functions={
        'https://w3id.org/um/openpredict/prediction': get_predictions,
        'https://w3id.org/um/openpredict/most_similar': most_similar,
    },
    title="SPARQL endpoint for OpenPredict functions", 
    description="A SPARQL endpoint to serve predictions generated using the OpenPredict classifier, using custom SPARQL functions. \n[Source code](https://github.com/MaastrichtU-IDS/openpredict-sparql-service)",
    version="0.0.1",
    public_url='https://service.openpredict.137.120.31.102.nip.io/sparql',
    cors_enabled=True,
    example_query=example_query
)
