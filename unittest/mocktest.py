# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch

class Person:
   def __init__(self, family_name, name, age):
       self.family_name = family_name
       self.name = name
       self.age  = age

   def full_name(self):
       return self.family_name + " " + self.name

   def is_adult(self):
       return True if self.age >= 20 else False

class Persons:
   def __init__(self, src):
      self.person_list = []
      for person_dict in src:
          self.person_list.append(Person(person_dict['family'], person_dict['name'], person_dict['age']))

   def get_adult_persons(self):
       result = []
       for person in self.person_list:
           if person.is_adult():
              result.append(person)
       return result

## 実際には実コードとテストコードは分離すること!!
class TestMock(unittest.TestCase):

   test_person_dicts = [
                         { 'family':'Son', 'name':'Gokuu', 'age':47 },
                         { 'family':'Son', 'name':'Gohan', 'age':27 },
                         { 'family':'Son', 'name':'Goten', 'age':17 },
                         { 'family':'Son', 'name':'Pan', 'age':5 },
                      ]

   # Mock対象はPerson.is_adult 
   # デコレータの場合、mockはメソッドの引数で受け取る
   @patch.object(Person, 'is_adult', return_value=True)
   def test_get_adult_persons_with_mock_decorator(self, mock_method):  

       adults = Persons(self.test_person_dicts).get_adult_persons()

       for person in adults:
           print("hello! " + person.full_name()) # full_name()はmock化されていない

       self.assertEqual(4, len(adults)) # 本来は2だが、mockの影響で変わる

       self.assertEqual(4, mock_method.call_count) # mockはcall時の引数なども記録している

  
   # コンキテストマネージャーを使った場合 
   def test_get_adult_persons_with_mock_context(self):

       # 呼び出し毎で値を変えたい場合や例外を返したい場合はside_effectを使う
       # side_effect = value/function/lambda
       returns = [False, False, False, True]
       with patch.object(Person, 'is_adult', side_effect=returns) as mock_method:
            adults = Persons(self.test_person_dicts).get_adult_persons()
            self.assertEqual(1, len(adults))

       self.assertEqual(4, mock_method.call_count)

if __name__ == '__main__':
    unittest.main()
