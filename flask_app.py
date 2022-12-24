from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

# Api nesnesinin oluşturulması
app = Flask(__name__)
api = Api(app)


class Books(Resource):

    # GET çağırıldığında books.csv okunması, dict formatına çevrilmesi ve döndürülmesi.
    def get(self):
        data = pd.read_csv('books.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    # POST çağırıldığında girdilerin parse edilmesi ve books.csv'ye bir satır eklenmesi.
    def post(self):
        title = request.args['Title']
        author = request.args['Author']
        genre = request.args['Genre']
        height = request.args['Height']
        publisher = request.args['Publisher']

        data = pd.read_csv('books.csv')

        new_data = pd.DataFrame({
            'Title': [title],
            'Author': [author],
            'Genre': [genre],
            'Height': [height],
            'Publisher': [publisher]
        })

        data = data.append(new_data, ignore_index=True)
        data.to_csv('books.csv', index=False)
        return {'data': new_data.to_dict('records')}, 200

    # Kitap adı ile silme işlemi
    def delete(self):
        title = request.args['Title']
        data = pd.read_csv('books.csv')
        data = data[data['Title'] != title]

        data.to_csv('books.csv', index=False)
        return {'message': 'Kayıt başarıyla silindi.'}, 200


# Yazarları getirme
class Authors(Resource):
    def get(self):
        data = pd.read_csv('books.csv', usecols=[1])
        data = data.to_dict('records')

        return {'data': data}, 200


# Türleri getirme
class Genres(Resource):
    def get(self):
        data = pd.read_csv('books.csv', usecols=[2])
        data = data.to_dict('records')

        return {'data': data}, 200





# GET işlemi için url adresleri
api.add_resource(Books, '/books')
api.add_resource(Authors, '/authors')
api.add_resource(Genres, '/genres')

if __name__ == '__main__':
    app.run()
