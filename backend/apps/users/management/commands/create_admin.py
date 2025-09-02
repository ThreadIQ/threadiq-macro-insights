from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser with admin privileges'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Admin username')
        parser.add_argument('--email', type=str, required=True, help='Admin email')
        parser.add_argument('--password', type=str, required=True, help='Admin password')
        parser.add_argument('--first-name', type=str, default='', help='First name')
        parser.add_argument('--last-name', type=str, default='', help='Last name')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists. Skipping creation.')
            )
            return

        # Check if user with email already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email "{email}" already exists. Skipping creation.')
            )
            return

        try:
            # Create the superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser "{username}" with email "{email}"'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to create superuser: {str(e)}')
            )
