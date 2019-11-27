import json
import urllib

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LibraryTests(APITestCase):
    content_type = "application/x-www-form-urlencoded"

    def has_content(self, parm_list, obj):
        return (set(parm_list) == set(obj.keys()))

    def create_book(self):
        url = '/api-v1/books/'
        send_data = {
            'author': 'TestAutor',
            'name': 'Name book '
        }
        response = self.client.post(
            url, urllib.parse.urlencode(send_data),
            content_type=self.content_type)
        return send_data, response

    def create_reader(self):
        url = '/api-v1/readers/'
        send_data = {'name': 'Name reader '}
        response = self.client.post(
            url, urllib.parse.urlencode(send_data),
            content_type=self.content_type)
        return send_data, response

    def test_root_request(self):
        url = '/api-v1/'
        response = self.client.get(url)
        exp_result = {
                    "readers": "http://testserver/api-v1/readers/",
                    "books": "http://testserver/api-v1/books/"
                    }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), exp_result)

    def test_books_get(self):
        url = '/api-v1/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        is_contents = self.has_content(
                                ['results', 'previous', 'next', 'count'], data)
        self.assertEqual(is_contents, True)

    def test_book_create_update_delete(self):
        send_data, response_post = self.create_book()
        self.assertEqual(response_post.status_code, 201)
        book_response = json.loads(response_post.content)
        is_contents = self.has_content(
            ['url', 'id', 'author', 'name', 'reader', 'reader_name'],
            book_response)
        self.assertEqual(is_contents, True)

        url = book_response.get('url')
        update_book = {
            'author': 'New author name',
            'name': book_response['name']
        }
        response_put = self.client.put(
                                url, urllib.parse.urlencode(update_book),
                                content_type=self.content_type)
        self.assertEqual(response_put.status_code, 200)

        book_response.update(update_book)
        self.assertEqual(
                        json.loads(response_put.content),
                        book_response)

        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, 204)

    def test_readers_get(self):
        url = '/api-v1/readers/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        is_contents = self.has_content(
                                ['results', 'previous', 'next', 'count'], data)
        self.assertEqual(is_contents, True)

    def test_readers_create_update_delete(self):
        send_data, response_post = self.create_reader()
        self.assertEqual(response_post.status_code, 201)
        reader_response = json.loads(response_post.content)
        is_contents = self.has_content(
            ['url', 'id', 'name'],
            reader_response)
        self.assertEqual(is_contents, True)

        url = reader_response.get('url')
        update_reader = {'name': 'new name'}
        response_put = self.client.put(
                                url, urllib.parse.urlencode(update_reader),
                                content_type=self.content_type)
        self.assertEqual(response_put.status_code, 200)

        reader_response.update(update_reader)
        self.assertEqual(
                        json.loads(response_put.content),
                        reader_response)

        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, 204)

    def test_add_reader_to_book(self):
        _, response_book = self.create_book()
        _, response_reader = self.create_reader()
        data_book = json.loads(response_book.content)
        data_reader = json.loads(response_reader.content)

        url = data_book.get('url')
        new_data = {'name': 'upd name',
                    'author': 'upd author',
                    'reader': data_reader.get('id')}
        response_put = self.client.put(
                                url, urllib.parse.urlencode(new_data),
                                content_type=self.content_type)
        self.assertEqual(response_put.status_code, 200)

        res_delete = self.client.delete(data_reader.get('url'))
        self.assertEqual(res_delete.status_code, 423)

        self.client.delete(data_book.get('url'))
        self.client.delete(data_reader.get('url'))
