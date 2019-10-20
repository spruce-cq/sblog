# services/resource/project/api/blog/models.py


from project.utils.basemodel import BaseModel, db


class Category(BaseModel):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    posts = db.relationship('Article', back_populates='category')

    _json_fields = ('id', 'name')

    def __repr__(self):
        return f'category: {self.name}'


class Article(BaseModel):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    body = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')

    _json_fields = ('id', 'title', 'body', 'timestamp', 'category', 'status')

    def __getitem__(self, item):
        if item == 'category':
            return self.category.id, self.category.name
        return getattr(self, item)

    def __repr__(self):
        return f'post: {self.title}'
