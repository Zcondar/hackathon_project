# from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

class Hackathon(Resource):
    
    def get(self):
        print("Calling service....")
        # use parser and find the user's query
        parser = reqparse.RequestParser()
        parser.add_argument('query')
        args = parser.parse_args()
        user_query = args['query']
        
        # Here need some algorithm
        '''
        This is a simple example, input a list of integer, output sum
        e.g.: (use space between the integer)
        input: "2 4 5 3 10"
        output: 24
        '''
        user_choices = user_query.split()
        numbers = [int(i) for i in user_choices]

        # need some prediction
        prediction = sum(numbers)
        
        # create JSON object
        output = {'return_value': str(prediction)}
        # output = {'return_value': '24'}
        
        return output
