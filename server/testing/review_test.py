from app import app, db
from server.models import Customer, Item, Review


class TestReview:
    '''Review model in models.py'''

    def test_can_be_instantiated(self):
        '''can be invoked to create a Python object.'''
        r = Review()
        assert r
        assert isinstance(r, Review)

    def test_has_comment(self):
        '''can be instantiated with a comment attribute.'''
        r = Review(comment='great product!')
        assert r.comment == 'great product!'

    def test_can_be_saved_to_database(self):
        '''can be added to a transaction and committed to review table with comment column.'''
    with app.app_context():
        assert 'comment' in Review.__table__.columns

        # Create and save a Customer and Item
        c = Customer(name='John Doe')
        i = Item(name='Sample Item', price=19.99)
        db.session.add_all([c, i])
        db.session.commit()

        # Now create a Review and associate it with the Customer and Item
        r = Review(comment='great!', customer=c, item=i)
        db.session.add(r)
        db.session.commit()

        # Ensure the Review is saved correctly and has an ID assigned
        assert hasattr(r, 'id')

        # Ensure the Review can be queried from the database by ID
        saved_review = db.session.query(Review).filter_by(id=r.id).first()
        assert saved_review is not None
        assert saved_review.comment == 'great!'


    def test_is_related_to_customer_and_item(self):
        '''has foreign keys and relationships'''
        with app.app_context():
            assert 'customer_id' in Review.__table__.columns
            assert 'item_id' in Review.__table__.columns

            c = Customer()
            i = Item()
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            # check foreign keys
            assert r.customer_id == c.id
            assert r.item_id == i.id
            # check relationships
            assert r.customer == c
            assert r.item == i
            assert r in c.reviews
            assert r in i.reviews
