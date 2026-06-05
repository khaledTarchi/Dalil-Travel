from app import create_app
from app.extensions import db
from app.models import User, Property, Meal, Booking

def init_db():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        print("Database tables created.")
        
        # Create Users
        admin = User(first_name='Admin', last_name='Dalil', email='admin@dalil.dz', password='password', role='admin')
        host1 = User(first_name='Omar', last_name='Tuareg', email='omar@desert.dz', password='password', role='host')
        host2 = User(first_name='Lamine', last_name='Oasis', email='lamine@oasis.dz', password='password', role='host')
        host3 = User(first_name='Kader', last_name='Djanet', email='kader@djanet.dz', password='password', role='host')
        
        db.session.add_all([admin, host1, host2, host3])
        db.session.commit()
        
        # Create Properties
        prop1 = Property(
            host_id=host1.id,
            title='Tassili N''Ajjer Eco-Camp',
            description='A traditional eco-camp located deep in the Tassili plateau. Sleep under the stars and experience true Tuareg hospitality.',
            region='Tassili',
            lat=25.5,
            lng=8.5,
            price_per_night=5000,
            image_url='/static/img/tassili_guesthouse.png',
            has_internet=False,
            power_source='Solar Panels',
            capacity=10,
            status='active'
        )
        
        prop2 = Property(
            host_id=host2.id,
            title='Brezina Clay Guesthouse',
            description='A beautiful guesthouse built with traditional clay architecture in the heart of Brezina oasis.',
            region='Brezina',
            lat=33.098,
            lng=1.261,
            price_per_night=7500,
            image_url='/static/img/brezina_guesthouse.png',
            has_internet=True,
            internet_quality='3G Weak',
            power_source='Grid and Generator',
            capacity=6,
            status='active'
        )
        
        prop3 = Property(
            host_id=host1.id,
            title='Timimoun Red Lodge',
            description='Experience the red oasis of Timimoun in our comfortable lodge with a panoramic view of the Sebkha.',
            region='Timimoun',
            lat=29.263,
            lng=0.230,
            price_per_night=6000,
            image_url='/static/img/timimoun_guesthouse.png',
            has_internet=True,
            internet_quality='4G Good',
            power_source='Grid',
            capacity=15,
            status='active'
        )
        
        prop4 = Property(
            host_id=host3.id,
            title='Djanet Oasis Camp',
            description='A magical camp nestled between the red rocks and golden dunes of Tadrart Rouge.',
            region='Djanet',
            lat=24.553,
            lng=9.484,
            price_per_night=8500,
            image_url='/static/img/djanet_guesthouse.png',
            has_internet=False,
            power_source='Solar Panels',
            capacity=8,
            status='active'
        )
        
        db.session.add_all([prop1, prop2, prop3, prop4])
        db.session.commit()
        
        # Create Meals
        meal1 = Meal(property_id=prop1.id, name='Desert Couscous', description='Traditional couscous with local vegetables and camel meat.', price=1500)
        meal2 = Meal(property_id=prop1.id, name='Mella Bread', description='Bread baked under hot sand and ashes.', price=300)
        meal3 = Meal(property_id=prop2.id, name='Merdoud', description='A rich, spicy pasta dish perfect for cold desert nights.', price=1200)
        meal4 = Meal(property_id=prop3.id, name='Stuffed Dates & Mint Tea', description='A sweet treat accompanied by traditional Tuareg tea.', price=500)
        meal5 = Meal(property_id=prop4.id, name='Tuareg Taguella', description='Authentic flatbread with sauce.', price=800)
        
        db.session.add_all([meal1, meal2, meal3, meal4, meal5])
        db.session.commit()
        
        print("Mock data seeded successfully.")

if __name__ == '__main__':
    init_db()
