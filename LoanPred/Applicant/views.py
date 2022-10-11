from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import ml


def home(request):
    return render(request, 'index.html')


def registerPage(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already exist')
                return render(request, 'regform.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already exist')
                return render(request, 'regform.html')
            else:
                print('REACHED HERE')
                # save data in db
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                print('user created')
                return redirect('/login/')

        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'regform.html')
    else:
        return render(request, 'regform.html')


def loginPage(request):
    if request.method == 'POST':
        # v = DoctorReg.objects.all()
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/prediction/')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'loginform.html')
    else:
        return render(request, 'loginform.html')


def predPage(request):
    if request.method == 'POST':
        applicantIncome = int(request.POST['applicantIncome'])
        coApplicantIncome = int(request.POST['coApplicantIncome'])
        is_married = int(request.POST.get('is_married', False))
        gender = int(request.POST.get('gender', False))
        dependents = int(request.POST['dependents'])
        is_graduated = int(request.POST['isGraduated'])
        is_selfEmployed = int(request.POST['isSelfEmployed'])
        is_historyPresent = int(request.POST['isHistoryPresent'])
        area_type = int(request.POST['area_type'])
        loan_amount = int(request.POST['loan_amount'])
        loan_duration = int(request.POST['loan_duration'])

        print("GENDER: ", gender)
        data = [applicantIncome, coApplicantIncome, loan_amount, loan_duration,
                is_historyPresent, int(gender == 0), int(gender == 1), int(is_married == 0), int(is_married == 1), int(dependents == 0), int(dependents == 1), int(dependents == 2), int(dependents >= 3), is_graduated, int(not is_graduated), int(not is_selfEmployed), is_selfEmployed, int(area_type == 1), int(area_type == 2), int(area_type == 3)]
        print(data)
        #data = [5432, 1234, 120, 360, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0]
        is_eligible = ml.output(data)
        if is_eligible == 'Y':
            return render(request, 'success.html')
        else:
            return render(request, 'failure.html')
    else:
        return render(request, 'predform.html')
