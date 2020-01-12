from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact



class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Adriano Ferrari',
            slug='adriano-ferrari',
            photo='/home/adriano/Documents/insync/images/pessoal/2012-11-15 23.45.15.jpg'
        )

    def test_email(self):
        contact = Contact.objects.create(speaker=self.speaker,
                                         kind='Contact.EMAIL',
                                         value='adriano-ferrari@outlook.com')
        self.assertTrue(Contact.objects.exists())

    def test_phone(self):
        contact = Contact.objects.create(speaker=self.speaker,
                                         kind='Contact.PHONE',
                                         value='11-996-040-987')
        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contant kind should be limited to E or P"""
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker=self.speaker,
                          kind='Contact.EMAIL',
                          value='adriano-ferrari@outlook.com')
        self.assertEqual('adriano-ferrari@outlook.com', str(contact))


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name='Adriano Ferrari',
            slug='adriano-ferrari',
            photo='/home/adriano/Documents/insync/images/pessoal/2012-11-15 23.45.15.jpg'
        )

        s.contact_set.create(kind=Contact.EMAIL, value='adriano-ferrari@outlook.com')
        s.contact_set.create(kind=Contact.PHONE, value='11-996-040-987')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['adriano-ferrari@outlook.com']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phones(self):
        qs = Contact.objects.phones()
        expected = ['11-996-040-987']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)
