#! /usr/bin/python
# -*- coding: utf-8 -*-


__author__ = ("Onur Kuru", "Osman Baskaya")
__date__ ="$Sep 20, 2011 00:43:16 PM$"

""" Movie Recommendation Systems """

from sys import stderr
 
try:
    from imdb import IMDb
except ImportError:
    stderr.write("imdbpy module does not exist " + 
                    "please make sure this module installed correctly.\n")
    exit(1)

from os import remove, path
from pickle import dump
import cProfile


persons = ['Steven Spielberg','Ridley Scott','Robert De Niro', 
                                'Robin Williams', 'Mel Gibson','Jim Carrey']

genres = ['comedy','history','sci-fi','drama','thriller','fantasy', 'western']

# our algorithm needs these in reversed order.
persons.reverse()
genres.reverse()

hash_table = dict()
ia = IMDb()

def remove_old_files(filelist):

    """This method helps to remove old files like db and hash_dump"""

    for filename in filelist:
        if path.exists(filename):
            try:
                remove(filename)
                print "%s deleted" % filename 
            except Exception: #TODO Exception spesifik.
                stderr.write("%s cannot remove. Please check your priviledge\n"
                                % filename)
                exit(1)

remove_old_files(('db.txt', 'hash_dump.txt')) 

#def fetch_movies(person, genre):
    #print "processing %s, %s" % (person, genre)
    #movies = get_movies(person, genre)
    #return movies

def get_movies(imdb_person, genre):
    any_error = False
    print "processing %s, %s" % (imdb_person, genre)
    try:
        all_work = imdb_person['genres'][genre]
    except KeyError:
        stderr.write("%s has no movie for %s\n" % (imdb_person, genre))
        any_error = True
    if not any_error:
        movies = [[work.movieID, work.data['title'].encode('utf-8'), imdb_person['name'].encode('utf-8'), genre] for work in all_work if work['kind'] == u'movie' ]
        yield movies

def update_hash(movies):
    for movie in movies:
        hash_table[movie[0]] = movie

def search_update_person(person):

    imdb_person = ia.search_person(person, results=2)[0]
    ia.update(imdb_person, info='genres links')
    print "%s updated" % person
    return imdb_person


def write_movies_to_db(movies):
    f = open('db.txt', 'a+')
    for movie in movies:
        line = ','.join(movie) + '\n'
        f.write(line)
    f.close()

def main():
    for person in persons:
        imdb_person = search_update_person(person)
        for genre in genres:
            for movies in get_movies(imdb_person, genre):
                if movies:
                    write_movies_to_db(movies)
                    update_hash(movies)
    dump(hash_table, open('hash_dump.txt', 'w'))

if __name__ == '__main__':
    cProfile.run('main()')
