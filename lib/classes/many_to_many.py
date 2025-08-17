class Author:
    def __init__(self, name):
        self._name = None
        self.name = name  # set once; then immutable

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Immutable after first valid set
        if self._name is not None:
            return
        if isinstance(value, str) and len(value) > 0:
            self._name = value

    # relationships
    def articles(self):
        return [article for article in Article.all if article.author is self]

    def magazines(self):
        # unique Magazine instances the author has written for
        seen = set()
        mags = []
        for article in self.articles():
            if article.magazine not in seen:
                seen.add(article.magazine)
                mags.append(article.magazine)
        return mags

    # associations
    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        # unique category strings for magazines the author has written for
        mags = self.magazines()
        if not mags:
            return None
        seen = set()
        areas = []
        for mag in mags:
            if mag.category not in seen:
                seen.add(mag.category)
                areas.append(mag.category)
        return areas


class Magazine:
    def __init__(self, name, category):
        self._name = None
        self._category = None
        self.name = name
        self.category = category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # must be str, 2..16 chars; can change after init
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        # ignore invalid sets

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        # must be non-empty str; can change after init
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        # ignore invalid sets

    # relationships
    def articles(self):
        return [article for article in Article.all if article.magazine is self]

    def contributors(self):
        # unique Author instances who have written for this magazine
        seen = set()
        authors = []
        for article in self.articles():
            if article.author not in seen:
                seen.add(article.author)
                authors.append(article.author)
        return authors

    # aggregates
    def article_titles(self):
        arts = self.articles()
        return [a.title for a in arts] if arts else None

    def contributing_authors(self):
        # authors with more than 2 articles for this magazine
        counts = {}
        for a in self.articles():
            counts[a.author] = counts.get(a.author, 0) + 1
        prolific = [author for author, n in counts.items() if n > 2]
        return prolific if prolific else None


class Article:
    all = []

    def __init__(self, author, magazine, title):
        self._author = None
        self._magazine = None
        self._title = None

        self.author = author      # use setter
        self.magazine = magazine  # use setter
        self.title = title        # use setter

        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if self._title is not None:
            return  # immutable after first set
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        # Must be Author instance; mutable
        if isinstance(value, Author):
            self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        # Must be Magazine instance; mutable
        if isinstance(value, Magazine):
            self._magazine = value

