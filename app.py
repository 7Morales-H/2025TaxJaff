import streamlit as st

def calculate_tax(property_value, budget_type):
    # Fixed rate and percentages
    rate_per_1000 = 32.80 / 1000  # $32.80 per $1000 of property value
    school_percentage = 0.50  # 50% for the school portion
    municipal_percentage = 0.32  # 32% for the municipal portion
    state_ed_percentage = 0.06  # 6% for the state education portion
    county_percentage = 0.12  # 12% for the county portion

    # Budget options
    budgets = {
        'current': 33760452,
        'new': 30760452,
        'default': 33858458
    }
    
    # Get the total budget for the selected budget type
    total_budget = budgets[budget_type]
    
    # Calculate the total property tax based on the rate per $1000
    total_tax = property_value * rate_per_1000

    # Adjust the school tax based on the budget scenario
    # School tax is 50% of the total tax, adjusted based on the total budget
    school_tax = total_tax * school_percentage * (total_budget / 33760452)  # Adjusted for budget
    
    # The municipal, state ed, and county portions remain fixed
    municipal_tax = total_tax * municipal_percentage
    state_ed_tax = total_tax * state_ed_percentage
    county_tax = total_tax * county_percentage
    
    # Calculate the total tax after adjusting the school tax
    total_tax_adjusted = school_tax + municipal_tax + state_ed_tax + county_tax

    # Return the breakdown of the tax calculations
    return {
        'total_tax': total_tax_adjusted,
        'school_tax': school_tax,
        'municipal_tax': municipal_tax,
        'state_ed_tax': state_ed_tax,
        'county_tax': county_tax
    }

def display_tax_scenarios(property_value):
    # Display tax calculations for each budget scenario
    st.write(f"Tax calculations for property value: ${property_value}")
    
    # Calculate total tax for the 'current' budget (used as base for rate of change)
    current_tax_details = calculate_tax(property_value, 'current')
    current_total_tax = current_tax_details['total_tax']
    
    # Loop through each budget scenario (new, default) and calculate tax details
    for budget_type in ['current', 'new', 'default']:
        tax_details = calculate_tax(property_value, budget_type)
        
        st.write(f"### Budget Scenario: {budget_type.capitalize()} Budget")
        st.write(f"Total Tax: ${tax_details['total_tax']:,.2f}")
        st.write(f"  - School Tax: ${tax_details['school_tax']:,.2f}")
        st.write(f"  - Municipal Tax: ${tax_details['municipal_tax']:,.2f}")
        st.write(f"  - State Ed Tax: ${tax_details['state_ed_tax']:,.2f}")
        st.write(f"  - County Tax: ${tax_details['county_tax']:,.2f}")
        
        # If it's not the 'current' budget, calculate the rate of change
        if budget_type != 'current':
            rate_of_change = tax_details['total_tax'] - current_total_tax
            st.write(f"Rate of Change: ${rate_of_change:,.2f}")
        st.write("-" * 40)

# Streamlit UI for property value input
st.title("Property Tax Calculator for Jaffrey, NH")
property_value = st.number_input("Enter your property value: $", min_value=0.0, step=1000.0)

# Display tax scenarios if the property value is provided
if property_value > 0:
    display_tax_scenarios(property_value)
