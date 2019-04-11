# import factory
#
# from demo_app import models
#
#
# class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
#     class Meta:
#         model = models.Category
#         sqlalchemy_session = models.db.session
#         sqlalchemy_session_persistence = 'flush'
#
#     name = factory.Sequence(lambda n: u'Category %d' % n)
#
#
# class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
#     class Meta:
#         model = models.Post
#         sqlalchemy_session = models.db.session
#         sqlalchemy_session_persistence = 'flush'
#
#     title = factory.Sequence(lambda n: u'Post Title %d' % n)
#     body = factory.Sequence(lambda n: u'Post Body %d' % n)
#     category = factory.SubFactory(CategoryFactory)
