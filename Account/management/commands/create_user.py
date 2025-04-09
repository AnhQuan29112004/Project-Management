import pandas as pd
from django.core.management.base import BaseCommand
from Account.models import CustomUser, UserProfile

class Command(BaseCommand):
    help = 'Create user accounts automatically from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True, help='Path to Excel file with user data')

    def handle(self, *args, **options):
        file_path = options['file']

        try:
            df = pd.read_excel(file_path)
            self.stdout.write(self.style.SUCCESS(f'Successfully read Excel file: {file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading Excel file: {str(e)}'))
            return

        required_columns = ['mssv', 'username', 'first_name', 'last_name', 'phone_number', 'birth', 'role']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            self.stdout.write(self.style.ERROR(f'Missing required columns: {missing_columns}'))
            return

        for index, row in df.iterrows():
            try:
                email = f"{row['last_name'].lower()}{row['mssv']}@huce.edu.vn"
                password = str(row['mssv'])

                if CustomUser.objects.filter(email=email).exists():
                    self.stdout.write(self.style.WARNING(f'User with email {email} already exists. Skipping...'))
                    continue

                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    username=row['username'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    phone_number=str(row['phone_number']),
                    birth=row['birth'],
                    role=row['role'],
                )

                UserProfile.objects.create(user=user)

                self.stdout.write(self.style.SUCCESS(f'Created user: {email} with password: {password}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating user at row {index + 2}: {str(e)}'))
                continue