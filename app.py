import streamlit as st

st.title("How many can go out?")

st.text('By Zero Six Data Science Consulting')
st.write("The recommendation is based on how many COVID cases are probably in your area, and the likelihood that at least one of your residents catches it.")

def incidence_rate(total_deaths_in_your_area, 
                                     num_people_area_of_cases, 
                                     num_people_neighborhood,
                                    fatality_rate = 6./100,
                                    days_from_infection_to_death=17,
                                    doubling_time=5.1):
    """
    Estimated true infection rate
    """
    
    number_of_times_double_cases = days_from_infection_to_death / doubling_time
  
    num_cases_cause_death = total_deaths_in_your_area / fatality_rate

    true_cases_today = num_cases_cause_death * (2**number_of_times_double_cases)

    infection_rate_now = true_cases_today / num_people_area_of_cases
    
    return infection_rate_now

def likelihood_of_at_least_one_covid(total_deaths_in_your_area, 
                                     num_people_area_of_cases, 
                                     num_people_neighborhood,
                                    fatality_rate = 6./100,
                                    days_from_infection_to_death=17,
                                    doubling_time=5.1):
    
    """
    Computes the likelihood of at least one having covid in a group of people within the area given death rates, 
    days from infection to death, and case doubling time
    """
  
    infection_rate_now = incidence_rate(total_deaths_in_your_area, 
                                     num_people_area_of_cases, 
                                     num_people_neighborhood,
                                    fatality_rate = 6./100,
                                    days_from_infection_to_death=17,
                                    doubling_time=5.1)

    likelihood_none_now = (1 - infection_rate_now)**num_people_neighborhood

    likelihood_at_least_one_now = 1 - likelihood_none_now

    return likelihood_at_least_one_now * 100

def allowed_out(deaths, popn, square_area=217.):
    """
    How many people should be allowed to go out?
    """
    
    people = 1
    proba = 0
    while proba <= 50:
        proba = int(likelihood_of_at_least_one_covid(deaths / square_area, popn / square_area, people / square_area)) * 100
        people += 1
    return people

st.sidebar.subheader("Parameters")

popn = st.sidebar.number_input('Number of people in your area:',
                                                   min_value=1, max_value=100000000, value=1000000)

deaths = st.sidebar.number_input('Number of deaths by covid in your area:', 
                                                   min_value=0, max_value=popn, value=1600)
square_area = st.sidebar.number_input("Land area in sq km:", min_value=1, max_value=popn, value=217)

allowed = allowed_out(deaths, popn, square_area)

allowed_percent = allowed * 100. / (popn / square_area)

st.subheader("Recommendation...")

st.write(f"Only **{int(allowed_percent)} percent** of people are allowed outside.")


st.title("How correct are the COVID-19 tests in your area?")


estimated_incidence_rate = incidence_rate(deaths, 
                                     popn, 
                                     popn,
                                    fatality_rate = 6./100,
                                    days_from_infection_to_death=17,
                                    doubling_time=5.1)

st.write(f"Estiamted true infection rate is **{int(estimated_incidence_rate * 100)}** percent. Hence...")

st.sidebar.subheader("COVID Test Metrics")

tp = st.sidebar.number_input('How right is the covid test at producing positive results when they actually have covid?', min_value=0, max_value=100, value=90)

fp = st.sidebar.number_input('How wrong is the covid test at producing positive results when they dont have covid?', min_value=0, max_value=100, value=10)

st.subheader("What is the probability that you ACTUALLY caught the virus?")

actual_tp = popn * estimated_incidence_rate * tp / 100
actual_fp = popn * (1 - estimated_incidence_rate) * (fp / 100)

actual_tpr = (actual_tp) / (actual_fp + actual_tp)

st.write(f"Probability of **actually catching the virus** after being tested positive is **{int(actual_tpr * 100)} percent**.")

actual_fn = popn * estimated_incidence_rate * (1-tp) / 100
actual_tn = popn * (1 - estimated_incidence_rate) * (1-fp) / 100

actual_tnr = (actual_tn / (actual_fn + actual_tn))

st.write(f"Probability of **NOT actually catching the virus** after being tested negative is **{int(actual_tnr * 100)} percent**.")
