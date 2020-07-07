import streamlit as st

st.title("How many can go out?")

st.text('By Zero Six Data Science Consulting')
st.write("The recommendation is based on how many COVID cases are probably in your area, and the likelihood that at least one of your residents catches it.")

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
  
    number_of_times_double_cases = days_from_infection_to_death / doubling_time
  
    num_cases_cause_death = total_deaths_in_your_area / fatality_rate

    true_cases_today = num_cases_cause_death * (2 ** number_of_times_double_cases)

    infection_rate_now = true_cases_today / num_people_area_of_cases

    likelihood_none_now = (1 - infection_rate_now)**num_people_neighborhood

    likelihood_at_least_one_now = 1 - likelihood_none_now

    return likelihood_at_least_one_now * 100

def allowed_out(deaths, popn, square_area=217.):
    people = 1
    proba = 0
    while proba <= 50:
        proba = int(likelihood_of_at_least_one_covid(deaths / square_area, popn / square_area, people / square_area)) * 100
        people += 1
    return people

st.sidebar.subheader("Parameters")

popn = st.sidebar.number_input('Number of people in your area:',
                                                   min_value=1, max_value=100000000, value=500000)

deaths = st.sidebar.number_input('Number of deaths by covid in your area:', 
                                                   min_value=0, max_value=popn, value=40)
square_area = st.sidebar.number_input("Land area in sqm:", min_value=1, max_value=popn, value=217)

allowed = allowed_out(deaths, popn, square_area)

st.subheader("Recommendation...")

st.write(f"Only {allowed} people per square km are allowed.")
