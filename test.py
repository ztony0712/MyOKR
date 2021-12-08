from app import app, db
from app.model import Group, User, Objective, KeyResult

import unittest
from io import BytesIO



class appTestCase(unittest.TestCase):


  def setUp(self):
    app.config.update(
      TESTING=True,
      WTF_CSRF_ENABLED=False,
      SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
      )
    db.create_all()
    self.client = app.test_client()
    self.runner = app.test_cli_runner()


  def tearDown(self):
    db.session.remove()
    db.drop_all()
  

  def user_signup(self):
    response = self.client.post('/signup', data=dict(
        username='ztony0712',
        email='ztony0712@outlook.com',
        password='zhaoy123.',
        ), follow_redirects=True)

    data = response.get_data(as_text=True)
    return data

  
  def test_index(self):
    response = self.client.get('/')
    data = response.get_data(as_text=True)
    self.assertIn('Free to try', data)


  def test_signup(self):
    response = self.client.get('/signup')
    data = response.get_data(as_text=True)
    self.assertIn('Registration', data)
  

  def test_signup_form_validation(self):
    response = self.client.post('/signup', data=dict(
      username='123',
      email='12345678@qq.com',
      password='12345678',
      ))
    data = response.get_data(as_text=True)
    self.assertIn('Incorrect format', data)

    response = self.client.post('/signup', data=dict(
      username='12345678',
      email='12345678@qq.com',
      password='123',
      ))
    data = response.get_data(as_text=True)
    self.assertIn('Incorrect format', data)

    response = self.client.post('/signup', data=dict(
      username='12345678',
      email='12345678qq.com',
      password='12345678',
      ))
    data = response.get_data(as_text=True)
    self.assertIn('Incorrect format', data)


  def test_user_signup(self):
    data = self.user_signup()
    self.assertIn('ztony0712', data)
    # test database
    user = User.query.filter_by(username='ztony0712').first()
    self.assertIsNotNone(user)
    self.assertEqual(user.email, 'ztony0712@outlook.com')

  def test_user_logout(self):
    self.user_signup()
    self.client.get('/logout')
    response = self.client.get('/login')
    data = response.get_data(as_text=True)
    self.assertIn('logged out', data)
  
  def test_existing_username(self):
    self.user_signup()
    self.client.get('/logout')

    response = self.client.post('/signup', data=dict(
        username='ztony0712',
        email='1140686961@outlook.com',
        password='zhaoy123.',
        ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Existing username', data)


  def test_existing_email(self):
    self.user_signup()
    self.client.get('/logout')
    response = self.client.post('/signup', data=dict(
        username='12345678',
        email='ztony0712@outlook.com',
        password='12345678',
        ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Existing email', data)


  def test_login(self):
    self.user_signup()
    self.client.get('/logout')
    self.client.get('/login')
    response = self.client.post('/login', data=dict(
      username='ztony0712',
      password='zhaoy123.',
      remember=False
      ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('ztony0712', data)


  def test_login_form_validation(self):
    response = self.client.post('/login', data=dict(
      username='ztony',
      password='zhaoy123.',
      remember=False
      ))
    data = response.get_data(as_text=True)
    self.assertIn('Incorrect format', data)

    response = self.client.post('/login', data=dict(
      username='ztony0712',
      password='zh',
      remember=False
      ))
    data = response.get_data(as_text=True)
    self.assertIn('Incorrect format', data)


  def test_no_existing_username(self):
    response = self.client.post('/login', data=dict(
      username='ztony0712',
      password='zhaoy123.',
      remember=False
      ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('No existing username', data)


  def test_incorrect_password(self):
    self.user_signup()
    self.client.get('/logout')
    response = self.client.post('/login', data=dict(
      username='ztony0712',
      password='12345678',
      remember=False
      ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Incorrect password', data)


  def test_change(self):
    self.user_signup()
    response = self.client.get('/change')
    data = response.get_data(as_text=True)
    self.assertIn('Old Password', data)


  def test_change_form_validation(self):
    self.user_signup()
    self.client.get('/logout')
    response = self.client.post('/change', data=dict(
      username='zt',
      oldpass='zhaoy123.',
      newPass='zhaoyimin123.'
      ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Incorrect format', data)

    response = self.client.post('/change', data=dict(
      username='ztony0712',
      oldpass='zh',
      newPass='zhaoyimin123.'
      ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Incorrect format', data)

    response = self.client.post('/change', data=dict(
      username='ztony0712',
      oldpass='zhaoy123.',
      newPass='zh'
      ), follow_redirects=True)
    self.client.get('/change')
    data = response.get_data(as_text=True)
    self.assertIn('Incorrect format', data)


  def test_change_no_existing_username(self):
    response = self.client.post('/change', data=dict(
      username='ztony0712',
      old_password='zhaoy123567',
      new_password='zhaoyimin123'
      ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('No existing username', data)


  def test_change_incorrect_password(self):
    self.user_signup()
    self.client.get('/logout')
    response = self.client.post('/change', data=dict(
      username='ztony0712',
      old_password='zhaoyimin123.',
      new_password='zhaoyimin123.'
      ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Incorrect old password', data)

  def test_my_okr_page(self):
    self.user_signup()
    response = self.client.get('/my_okr')
    data = response.get_data(as_text=True)
    self.assertIn('ztony0712', data)

  def test_add_objective_form_validation(self):
    self.user_signup()
    response = self.client.post('/add', data=dict(
      title=''
      ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Failed to Add objective', data)

  def test_add_key_result_form_validation(self):
    self.user_signup()
    self.client.post('/add', data=dict(
      title='test'
    ), follow_redirects=True)
    response = self.client.post('/enrich/1', data=dict(
      dcp=''
    ), follow_redirects=True)

    data = response.get_data(as_text=True)
    self.assertIn('Failed to add Key Result', data)
  
  def test_create_group_form_validation(self):
    self.user_signup()
    self.client.post('/create')
    response = self.client.post('/group_submit', data=dict(
      title=''
    ), follow_redirects=True)

    data = response.get_data(as_text=True)
    self.assertIn('Incorrect format', data)

  def test_description_form_validation(self):
    self.user_signup()
    self.client.post('/add', data=dict(
      title='test'
    ), follow_redirects=True)
    self.client.post('/enrich/1', data=dict(
      dcp='test'
    ), follow_redirects=True)

    self.client.get('/edit/1')
    response = self.client.post('/okr_submit/1', data=dict(
      title='',
      dcp = 'test',
      date = '2021-12-09',
      now = 1,
      total = 1,
      step = 1,
      urgency = 'Neturalized',
      note = 'test'
    ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Failed to submit modification', data)

    self.client.get('/edit/1')
    response = self.client.post('/okr_submit/1', data=dict(
      title='test',
      dcp='',
      date='2021-12-09',
      now=1,
      total=1,
      step=1,
      urgency='Neturalized',
      note='test'
    ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Failed to submit modification', data)

    self.client.get('/edit/1')
    response = self.client.post('/okr_submit/1', data=dict(
      title='test',
      dcp='test',
      date='',
      now=1,
      total=1,
      step=1,
      urgency='Neturalized',
      note='test'
    ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Failed to submit modification', data)

    self.client.get('/edit/1')
    response = self.client.post('/okr_submit/1', data=dict(
      title='test',
      dcp='test',
      date='2021-12-09',
      now=-1,
      total=1,
      step=1,
      urgency='Neturalized',
      note='test'
    ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Failed to submit modification', data)

    self.client.get('/edit/1')
    response = self.client.post('/okr_submit/1', data=dict(
      title='test',
      dcp='test',
      date='2021-12-09',
      now=1,
      total=-1,
      step=1,
      urgency='Neturalized',
      note='test'
    ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Failed to submit modification', data)

    self.client.get('/edit/1')
    response = self.client.post('/okr_submit/1', data=dict(
      title='test',
      dcp='test',
      date='2021-12-09',
      now=1,
      total=1,
      step=-1,
      urgency='Neturalized',
      note='test'
    ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Failed to submit modification', data)

    self.client.get('/edit/1')
    response = self.client.post('/okr_submit/1', data=dict(
      title='test',
      dcp='test',
      date='2021-12-09',
      now=1,
      total=1,
      step=1,
      urgency='',
      note='test'
    ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Failed to submit modification', data)

  def test_del_objective_btn(self):
    self.user_signup()
    self.client.post('/add', data=dict(
      title='test'
      ), follow_redirects=True)
    self.client.get('/delete_obj/1')
    response = self.client.get('/my_okr')
    data = response.get_data(as_text=True)
    self.assertIn('Delete Objective', data)

    obj = Objective.query.filter_by(title='test').first()
    self.assertIsNone(obj)

  def test_del_key_result_btn(self):
    self.user_signup()
    self.client.post('/add', data=dict(
      title='test'
    ), follow_redirects=True)
    self.client.post('/enrich/1', data=dict(
      dcp='test'
    ), follow_redirects=True)

    self.client.get('/delete_kr/1')
    response = self.client.get('/my_okr')
    data = response.get_data(as_text=True)
    self.assertIn('Delete Key Result', data)

    kr = KeyResult.query.filter_by(dcp='test').first()
    self.assertIsNone(kr)

  def test_join_and_quit_btn(self):
    self.user_signup()
    response = self.client.post('/group_submit', data=dict(
      group_name='test'
    ), follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('test', data)
    self.client.get('/logout')

    self.client.post('/signup', data=dict(
      username='adore0712',
      email='adore@outlook.com',
      password='zhaoy123.',
    ), follow_redirects=True)

    response = self.client.get('/join_submit/1', follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Join in a group', data)
    gp = Group.query.filter_by(group_name='test').first()
    self.assertIsNotNone(gp)

    response = self.client.get('/quit_submit/1', follow_redirects=True)
    data = response.get_data(as_text=True)
    self.assertIn('Quit a group', data)


