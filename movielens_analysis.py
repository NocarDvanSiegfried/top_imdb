import os
from collections import Counter
import pytest
import sys

class Movies:
    def __init__(self, source):
        self.movies = []
        self.years = set()
        try:
            if isinstance(source, str):
                import os
                tried_paths = [source]
                f = None
                try:
                    f = open(source, 'r', encoding='utf-8')
                except FileNotFoundError:
                    alt_path = os.path.join(os.path.pardir, source)
                    tried_paths.append(alt_path)
                    try:
                        f = open(alt_path, 'r', encoding='utf-8')
                    except FileNotFoundError:
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        alt_path2 = os.path.join(script_dir, source)
                        tried_paths.append(alt_path2)
                        try:
                            f = open(alt_path2, 'r', encoding='utf-8')
                        except FileNotFoundError:
                            raise FileNotFoundError(f"Не найден файл {source}. Пробовал пути: {tried_paths}")
                with f:
                    self._load_data(f)
            else:
                self._load_data(source)
        except (IOError, OSError) as e:
            raise Exception(f"Failed to load movies data: {str(e)}")
    
    def _load_data(self, file_obj):
        try:
            next(file_obj)
            for i, line in enumerate(file_obj):
                try:
                    parts = line.strip().split(',', 2)
                    if len(parts) < 3:
                        continue
                    movieId, title, genres = parts
                    year = None
                    if '(' in title and ')' in title:
                        y = title.split('(')[-1].split(')')[0]
                        if y.isdigit():
                            year = y
                            self.years.add(int(year))
                    self.movies.append({
                        'movieId': movieId,
                        'title': title,
                        'genres': genres,
                        'year': year
                    })
                except ValueError as e:
                    raise Exception(f"Invalid data format in line {i+2}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading movies data: {str(e)}")
    
    def get_movies(self):
        return self.movies
    
    def get_movie(self, movie_id):
        for movie in self.movies:
            if str(movie['movieId']) == str(movie_id):
                return movie
        return None
    
    def get_movie_by_title(self, title):
        for movie in self.movies:
            if movie['title'].lower() == title.lower():
                return movie
        return None
    
    def get_genres(self):
        genres = set()
        for movie in self.movies:
            genres.update(movie['genres'].split('|'))
        return sorted(list(genres))
    
    def get_year_range(self):
        if self.years:
            return min(self.years), max(self.years)
        return None, None

class Links:
    def __init__(self, source, movies_obj):
        self.links = []
        self.movies_obj = movies_obj
        self.movieid_to_link = {}
        self.title_to_link = {}
        try:
            if isinstance(source, str):
                import os
                tried_paths = [source]
                f = None
                try:
                    f = open(source, 'r', encoding='utf-8')
                except FileNotFoundError:
                    alt_path = os.path.join(os.path.pardir, source)
                    tried_paths.append(alt_path)
                    try:
                        f = open(alt_path, 'r', encoding='utf-8')
                    except FileNotFoundError:
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        alt_path2 = os.path.join(script_dir, source)
                        tried_paths.append(alt_path2)
                        try:
                            f = open(alt_path2, 'r', encoding='utf-8')
                        except FileNotFoundError:
                            raise FileNotFoundError(f"Не найден файл {source}. Пробовал пути: {tried_paths}")
                with f:
                    self._load_data(f)
            else:
                self._load_data(source)
        except (IOError, OSError) as e:
            raise Exception(f"Failed to load links data: {str(e)}")
    
    def _load_data(self, file_obj):
        try:
            next(file_obj)
            for i, line in enumerate(file_obj):
                try:
                    parts = line.strip().split(',')
                    if len(parts) < 3:
                        continue
                    movieId, imdbId, tmdbId = parts
                    link = {'movieId': movieId, 'imdbId': imdbId, 'tmdbId': tmdbId}
                    self.links.append(link)
                    self.movieid_to_link[movieId] = link
                    movie = self.movies_obj.get_movie(movieId)
                    if movie:
                        self.title_to_link[movie['title'].lower()] = link
                except ValueError as e:
                    raise Exception(f"Invalid data format in line {i+2}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading links data: {str(e)}")
    
    def get_links(self):
        return self.links
    
    def get_movie_links(self, movie_id):
        return self.movieid_to_link.get(str(movie_id), None)
    
    def get_link_by_title(self, title):
        return self.title_to_link.get(title.lower(), None)
    
    def get_imdb_link(self, movie_id):
        link = self.get_movie_links(movie_id)
        if link:
            imdb_id = link['imdbId']
            return f"https://www.imdb.com/title/tt{str(imdb_id).zfill(7)}/"
        return ""

class Ratings:
    def __init__(self, source, movies_obj):
        self.ratings = []
        self.movies_obj = movies_obj
        self.movieid_to_ratings = {}
        self.title_to_ratings = {}
        try:
            if isinstance(source, str):
                import os
                tried_paths = [source]
                f = None
                try:
                    f = open(source, 'r', encoding='utf-8')
                except FileNotFoundError:
                    alt_path = os.path.join(os.path.pardir, source)
                    tried_paths.append(alt_path)
                    try:
                        f = open(alt_path, 'r', encoding='utf-8')
                    except FileNotFoundError:
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        alt_path2 = os.path.join(script_dir, source)
                        tried_paths.append(alt_path2)
                        try:
                            f = open(alt_path2, 'r', encoding='utf-8')
                        except FileNotFoundError:
                            raise FileNotFoundError(f"Не найден файл {source}. Пробовал пути: {tried_paths}")
                with f:
                    self._load_data(f)
            else:
                self._load_data(source)
        except (IOError, OSError) as e:
            raise Exception(f"Failed to load ratings data: {str(e)}")
    
    def _load_data(self, file_obj):
        try:
            next(file_obj)
            for i, line in enumerate(file_obj):
                try:
                    parts = line.strip().split(',')
                    if len(parts) < 4:
                        continue
                    userId, movieId, rating, timestamp = parts
                    r = {'userId': userId, 'movieId': movieId, 'rating': float(rating), 'timestamp': int(timestamp)}
                    self.ratings.append(r)
                    self.movieid_to_ratings.setdefault(movieId, []).append(r)
                    movie = self.movies_obj.get_movie(movieId)
                    if movie:
                        self.title_to_ratings.setdefault(movie['title'].lower(), []).append(r)
                except ValueError as e:
                    raise Exception(f"Invalid data format in line {i+2}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading ratings data: {str(e)}")
    
    def get_ratings(self):
        return self.ratings
    
    def get_movie_ratings(self, movie_id):
        return self.movieid_to_ratings.get(str(movie_id), [])
    
    def get_ratings_by_title(self, title):
        return self.title_to_ratings.get(title.lower(), [])
    
    def get_average_rating(self, movie_id):
        ratings = self.get_movie_ratings(movie_id)
        if not ratings:
            return 0.0
        return sum(r['rating'] for r in ratings) / len(ratings)
    
    def get_median_rating(self, movie_id):
        ratings = [r['rating'] for r in self.get_movie_ratings(movie_id)]
        if not ratings:
            return 0.0
        ratings.sort()
        n = len(ratings)
        mid = n // 2
        if n % 2:
            return ratings[mid]
        return (ratings[mid-1] + ratings[mid]) / 2
    
    def top_by_ratings(self, n=10, method='mean'):
        movie_scores = []
        for movie in self.movies_obj.get_movies():
            ratings = self.get_movie_ratings(movie['movieId'])
            if ratings:
                values = [r['rating'] for r in ratings]
                if method == 'mean':
                    score = sum(values) / len(values)
                elif method == 'median':
                    values.sort()
                    mid = len(values) // 2
                    score = values[mid] if len(values) % 2 else (values[mid-1] + values[mid]) / 2
                else:
                    continue
                movie_scores.append((movie, score))
        return sorted(movie_scores, key=lambda x: x[1], reverse=True)[:n]

class Tags:
    def __init__(self, source, movies_obj):
        self.tags = []
        self.movies_obj = movies_obj
        self.movieid_to_tags = {}
        self.title_to_tags = {}
        try:
            if isinstance(source, str):
                import os
                tried_paths = [source]
                f = None
                try:
                    f = open(source, 'r', encoding='utf-8')
                except FileNotFoundError:
                    alt_path = os.path.join(os.path.pardir, source)
                    tried_paths.append(alt_path)
                    try:
                        f = open(alt_path, 'r', encoding='utf-8')
                    except FileNotFoundError:
                        script_dir = os.path.dirname(os.path.abspath(__file__))
                        alt_path2 = os.path.join(script_dir, source)
                        tried_paths.append(alt_path2)
                        try:
                            f = open(alt_path2, 'r', encoding='utf-8')
                        except FileNotFoundError:
                            raise FileNotFoundError(f"Не найден файл {source}. Пробовал пути: {tried_paths}")
                with f:
                    self._load_data(f)
            else:
                self._load_data(source)
        except (IOError, OSError) as e:
            raise Exception(f"Failed to load tags data: {str(e)}")
    
    def _load_data(self, file_obj):
        try:
            next(file_obj)
            for i, line in enumerate(file_obj):
                try:
                    parts = line.strip().split(',')
                    if len(parts) < 4:
                        continue
                    userId, movieId, tag, timestamp = parts
                    t = {'userId': userId, 'movieId': movieId, 'tag': tag, 'timestamp': int(timestamp)}
                    self.tags.append(t)
                    self.movieid_to_tags.setdefault(movieId, []).append(t)
                    movie = self.movies_obj.get_movie(movieId)
                    if movie:
                        self.title_to_tags.setdefault(movie['title'].lower(), []).append(t)
                except ValueError as e:
                    raise Exception(f"Invalid data format in line {i+2}: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading tags data: {str(e)}")
    
    def get_tags(self):
        return self.tags
    
    def get_movie_tags(self, movie_id):
        return self.movieid_to_tags.get(str(movie_id), [])
    
    def get_tags_by_title(self, title):
        return self.title_to_tags.get(title.lower(), [])

TEST_MOVIES_DATA = """movieId,title,genres
1,Toy Story (1995),Adventure|Animation|Children|Comedy|Fantasy
2,Jumanji (1995),Adventure|Children|Fantasy
3,Grumpier Old Men (1995),Comedy|Romance"""

TEST_RATINGS_DATA = """userId,movieId,rating,timestamp
1,1,4.5,1147880044
1,2,3.0,1147880044
2,1,5.0,1147880044"""

TEST_TAGS_DATA = """userId,movieId,tag,timestamp
1,1,pixar,1147880044
2,1,animation,1147880044
3,2,fantasy,1147880044"""

TEST_LINKS_DATA = """movieId,imdbId,tmdbId
1,114709,862
2,113497,8844
3,113228,15602"""

@pytest.fixture
def setup_classes():
    test_files = {
        'test_movies.csv': TEST_MOVIES_DATA,
        'test_ratings.csv': TEST_RATINGS_DATA,
        'test_tags.csv': TEST_TAGS_DATA,
        'test_links.csv': TEST_LINKS_DATA
    }
    
    try:
        for filename, content in test_files.items():
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        
        movies = Movies('test_movies.csv')
        ratings = Ratings('test_ratings.csv', movies)
        tags = Tags('test_tags.csv', movies)
        links = Links('test_links.csv', movies)
        
        yield movies, ratings, tags, links
    finally:
        for filename in test_files:
            try:
                os.remove(filename)
            except OSError:
                pass

def test_movies_types(setup_classes):
    movies, _, _, _ = setup_classes
    
    movies_list = movies.get_movies()
    assert isinstance(movies_list, list)
    assert all(isinstance(movie, dict) for movie in movies_list)
    assert len(movies_list) == 3
    
    movie = movies.get_movie(1)
    assert isinstance(movie, dict)
    assert movie['title'] == 'Toy Story (1995)'
    
    genres = movies.get_genres()
    assert isinstance(genres, list)
    assert all(isinstance(genre, str) for genre in genres)
    assert genres == sorted(genres)
    assert 'Adventure' in genres

def test_ratings_types(setup_classes):
    _, ratings, _, _ = setup_classes
    
    ratings_list = ratings.get_ratings()
    assert isinstance(ratings_list, list)
    assert all(isinstance(rating, dict) for rating in ratings_list)
    assert len(ratings_list) == 3
    
    movie_ratings = ratings.get_movie_ratings(1)
    assert isinstance(movie_ratings, list)
    assert len(movie_ratings) == 2
    
    avg_rating = ratings.get_average_rating(1)
    assert isinstance(avg_rating, float)
    assert avg_rating == 4.75

def test_tags_types(setup_classes):
    _, _, tags, _ = setup_classes
    
    tags_list = tags.get_tags()
    assert isinstance(tags_list, list)
    assert all(isinstance(tag, dict) for tag in tags_list)
    assert len(tags_list) == 3
    
    movie_tags = tags.get_movie_tags(1)
    assert isinstance(movie_tags, list)
    assert len(movie_tags) == 2
    
    common_tags = tags.get_tags_by_title('toy story (1995)')
    assert isinstance(common_tags, list)
    assert all(isinstance(tag, dict) for tag in common_tags)
    assert all(isinstance(tag['tag'], str) for tag in common_tags)

def test_links_types(setup_classes):
    _, _, _, links = setup_classes
    
    links_list = links.get_links()
    assert isinstance(links_list, list)
    assert all(isinstance(link, dict) for link in links_list)
    assert len(links_list) == 3
    
    movie_links = links.get_movie_links(1)
    assert isinstance(movie_links, dict)
    assert movie_links['imdbId'] == '114709'
    
    imdb_link = links.get_imdb_link(1)
    assert isinstance(imdb_link, str)
    assert imdb_link == 'https://www.imdb.com/title/tt0114709/'

def test_error_handling(setup_classes):
    movies, ratings, tags, links = setup_classes
    
    assert movies.get_movie("invalid") is None
    assert ratings.get_movie_ratings("invalid") == []
    assert tags.get_movie_tags("invalid") == []
    assert links.get_movie_links("invalid") is None
    assert tags.get_tags_by_title("invalid") == []

if __name__ == "__main__":
    import sys
    from datetime import datetime
    from collections import Counter
    import os
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("python movielens_analysis.py top [N] [mean|median]")
        print("python movielens_analysis.py movie [ID|TITLE]")
        print("python movielens_analysis.py genre [GENRE]")
        print("python movielens_analysis.py year [YEAR]")
        print("python movielens_analysis.py user [USER_ID]")
        print("python movielens_analysis.py tag [TAG]")
        print("python movielens_analysis.py imdb [ID|TITLE]")
        print("python movielens_analysis.py stats")
        print("python movielens_analysis.py years")
        sys.exit(1)
        
    command = sys.argv[1]
    movies = Movies('datasets/ml-latest-small/movies.csv')
    ratings = Ratings('datasets/ml-latest-small/ratings.csv', movies)
    tags = Tags('datasets/ml-latest-small/tags.csv', movies)
    links = Links('datasets/ml-latest-small/links.csv', movies)
    
    if command == "top":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        method = sys.argv[3] if len(sys.argv) > 3 else 'mean'
        top = ratings.top_by_ratings(n, method)
        for movie, score in top:
            print(f"{movie['title']} - {method}: {score:.2f}")
            
    elif command == "movie":
        if len(sys.argv) < 3:
            print("Provide movie ID or title")
            sys.exit(1)
        key = sys.argv[2]
        movie = movies.get_movie(key) or movies.get_movie_by_title(key)
        if not movie:
            print("Movie not found")
            sys.exit(1)
        print(f"Title: {movie['title']}")
        print(f"Genres: {movie['genres']}")
        print(f"Year: {movie['year']}")
        print(f"Average rating: {ratings.get_average_rating(movie['movieId']):.2f}")
        print(f"Median rating: {ratings.get_median_rating(movie['movieId']):.2f}")
        print(f"IMDB: {links.get_imdb_link(movie['movieId'])}")
        print(f"Tags: {[t['tag'] for t in tags.get_movie_tags(movie['movieId'])]}")
        
    elif command == "genre":
        if len(sys.argv) < 3:
            print("Provide genre")
            sys.exit(1)
        genre = sys.argv[2]
        for movie in movies.get_movies():
            if genre in movie['genres']:
                print(f"{movie['title']}")
        
    elif command == "year":
        if len(sys.argv) < 3:
            min_year, max_year = movies.get_year_range()
            print(f"Provide year between {min_year} and {max_year}")
            sys.exit(1)
        year = sys.argv[2]
        found = False
        count = 0
        for movie in movies.get_movies():
            if movie['year'] == year:
                print(f"{movie['title']}")
                found = True
                count += 1
        if not found:
            print(f"Нет фильмов за {year}")
        else:
            print(f"Всего фильмов за {year}: {count}")
        
    elif command == "user":
        if len(sys.argv) < 3:
            print("Provide user ID")
            sys.exit(1)
        user_id = sys.argv[2]
        for r in ratings.get_ratings():
            if r['userId'] == user_id:
                movie = movies.get_movie(r['movieId'])
                if movie:
                    print(f"{movie['title']}: {r['rating']}")
        
    elif command == "tag":
        if len(sys.argv) < 3:
            print("Provide tag")
            sys.exit(1)
        tag = sys.argv[2].lower()
        for t in tags.get_tags():
            if tag in t['tag'].lower():
                movie = movies.get_movie(t['movieId'])
                if movie:
                    print(f"{movie['title']}")
        
    elif command == "imdb":
        if len(sys.argv) < 3:
            print("Provide IMDB id or movie title")
            sys.exit(1)
        key = sys.argv[2]
        link = links.get_movie_links(key) or links.get_link_by_title(key)
        if link:
            print(f"IMDB: https://www.imdb.com/title/tt{str(link['imdbId']).zfill(7)}/")
        else:
            print("Not found")
        
    elif command == "stats":
        print(f"Movies: {len(movies.get_movies())}")
        print(f"Ratings: {len(ratings.get_ratings())}")
        print(f"Tags: {len(tags.get_tags())}")
        print(f"Years: {movies.get_year_range()}")
        
    elif command == "years":
        min_year, max_year = movies.get_year_range()
        print(f"Years: {min_year} - {max_year}")
        
    else:
        print("Unknown command") 