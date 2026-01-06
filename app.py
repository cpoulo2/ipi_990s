# Exploring Illinois Policy Institute 990 Data

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px

# Load data
@st.cache_data
def load_data():

    try:
        df_expenses = pd.read_csv('total_expenses.csv')
        df_schedule_i = pd.read_csv('schedule_i.csv')
        df_contractors = pd.read_csv('part_vii_b.csv')
        df_schedule_j = pd.read_csv('schedule_j.csv')
        return df_expenses, df_schedule_i, df_contractors, df_schedule_j
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}. Please ensure the CSV files are in the correct location.")
        return None, None, None, None

# Streamlit app title

def main():    

    st.set_page_config(
        page_title="Illinois Policy Institute 990 Data Explorer", 
        layout="wide",
        page_icon="💵",
        initial_sidebar_state="collapsed"
    )

    st.markdown('<h1 style="font-family:Arial, Helvetica, sans-serif;">Illinois Policy Institute (IPI) 990 Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown('''<h2 style="font-size:20px; font-family:Arial, Helvetica, sans-serif;">
    
We are using the IPI 990 Data Explorer to draw out key insights into how IPI spends it's money and the networks of non-profits and independent contractors IPI contributes to and is connected to. This will be used to inform our "follow an IPI dollar" research project.

The IPI 990 Data Explorer combines data from about 3,000 IRS Form 990s filed by IPI, IPI's grantees, and the grantees of those grantees. Form 990s are IRS required returns for tax-exempt organizations. Using these forms we look at the following data between 2013-2024: 
- total expenses; 
- the amount of grants awarded to other organizations (Schedule I);
- independent contractor expenses (Part VII-B); and
- compensation information for certain officers, directors, trustees, key employees, and highest compensated employees (Schedule J).</h2>

''',unsafe_allow_html=True)

    df_expenses, df_schedule_i, df_contractors, df_schedule_j = load_data()

    # take total amount in 2024

    total_2024 = df_schedule_i[df_schedule_i['tax_year'] == '2024-12-31']['grantee_cash_grant'].sum()
    st.markdown(f'''<h2 style="font-size:20px; font-family:Arial, Helvetica, sans-serif;">Total Grants Given in the IPI Network (2024): ${total_2024:,.2f}</h2>''', unsafe_allow_html=True)

    # Make all filing_org names consistent

    names = df_expenses.groupby(['filing_ein']).agg(
        filing_org=('filing_org','first')
    )

    # 3 orgs do not have filing names. Manually add

    # if 133859811 then filing_org = "THE COMMON GOOD INSTITUTE INC"
    # if 221539721 then filing_org = "THE SEEING EYE INC"
    # if 391134735 then filing_org = "MILWAUKEE BALLET COMPANY INC"

    names.loc[133859811, 'filing_org'] = "THE COMMON GOOD INSTITUTE INC"
    names.loc[221539721, 'filing_org'] = "THE SEEING EYE INC"
    names.loc[391134735, 'filing_org'] = "MILWAUKEE BALLET COMPANY INC"

    # filter for missing filing org name

    names['filing_org'] = [x.upper() for x in names['filing_org']]

    name_dict = names['filing_org'].to_dict()

    # in all data frames replace the filing org name with the name_dict
    df_expenses['filing_org'] = df_expenses['filing_ein'].map(name_dict)

    # repeat this step for the other dataframes
    #schedule i

    names = df_schedule_i.groupby(['filing_ein']).agg(
        filing_org=('filing_org','first')
    )

    # 3 orgs do not have filing names. Manually add

    # if 133859811 then filing_org = "THE COMMON GOOD INSTITUTE INC"
    # if 221539721 then filing_org = "THE SEEING EYE INC"
    # if 391134735 then filing_org = "MILWAUKEE BALLET COMPANY INC"

    names.loc[133859811, 'filing_org'] = "THE COMMON GOOD INSTITUTE INC"
    names.loc[221539721, 'filing_org'] = "THE SEEING EYE INC"
    names.loc[391134735, 'filing_org'] = "MILWAUKEE BALLET COMPANY INC"

    names['filing_org'] = [x.upper() for x in names['filing_org']]

    name_dict = names['filing_org'].to_dict()

    # in all data frames replace the filing org name with the name_dict
    df_schedule_i['filing_org'] = df_schedule_i['filing_ein'].map(name_dict)

    #schedule i (also dp grantee_business_name)

    names = df_schedule_i.groupby(['grantee_ein']).agg(
        grantee_business_name=('grantee_business_name','first')
    )

    # create missing grantee_business_name entries df

    missing = names[names['grantee_business_name'].isnull()]

    # 3 orgs do not have filing names. Manually add

    # if 133859811 then grantee_business_name = "THE COMMON GOOD INSTITUTE INC"
    # if 221539721 then grantee_business_name = "THE SEEING EYE INC"
    # if 391134735 then grantee_business_name = "MILWAUKEE BALLET COMPANY INC"

    names.loc[133859811, 'grantee_business_name'] = "THE COMMON GOOD INSTITUTE INC"
    names.loc[221539721, 'grantee_business_name'] = "THE SEEING EYE INC"
    names.loc[391134735, 'grantee_business_name'] = "MILWAUKEE BALLET COMPANY INC"


    names['grantee_business_name'] = [x.upper() if x is not None else None for x in names['grantee_business_name']]

    name_dict = names['grantee_business_name'].to_dict()

    # in all data frames replace the filing org name with the name_dict
    df_schedule_i['grantee_business_name'] = df_schedule_i['grantee_ein'].map(name_dict)


    #schedule j

    names = df_schedule_j.groupby(['filing_ein']).agg(
        filing_org=('filing_org','first')
    )

    # 3 orgs do not have filing names. Manually add

    # if 133859811 then filing_org = "THE COMMON GOOD INSTITUTE INC"
    # if 221539721 then filing_org = "THE SEEING EYE INC"
    # if 391134735 then filing_org = "MILWAUKEE BALLET COMPANY INC"

    names.loc[133859811, 'filing_org'] = "THE COMMON GOOD INSTITUTE INC"
    names.loc[221539721, 'filing_org'] = "THE SEEING EYE INC"
    names.loc[391134735, 'filing_org'] = "MILWAUKEE BALLET COMPANY INC"

    names['filing_org'] = [x.upper() for x in names['filing_org']]

    name_dict = names['filing_org'].to_dict()

    # in all data frames replace the filing org name with the name_dict
    df_schedule_j['filing_org'] = df_schedule_j['filing_ein'].map(name_dict)

    #contractors

    names = df_contractors.groupby(['filing_ein']).agg(
        filing_org=('filing_org','first')
    )

    # 3 orgs do not have filing names. Manually add

    # if 133859811 then filing_org = "THE COMMON GOOD INSTITUTE INC"
    # if 221539721 then filing_org = "THE SEEING EYE INC"
    # if 391134735 then filing_org = "MILWAUKEE BALLET COMPANY INC"

    names.loc[133859811, 'filing_org'] = "THE COMMON GOOD INSTITUTE INC"
    names.loc[221539721, 'filing_org'] = "THE SEEING EYE INC"
    names.loc[391134735, 'filing_org'] = "MILWAUKEE BALLET COMPANY INC"

    names['filing_org'] = [x.upper() for x in names['filing_org']]

    name_dict = names['filing_org'].to_dict()

    # in all data frames replace the filing org name with the name_dict
    df_contractors['filing_org'] = df_contractors['filing_ein'].map(name_dict)    

    # Group by year and filing_ein for each data source (without totals yet)

    exp = df_expenses.groupby(['tax_year','filing_ein']).agg(
        total_expenses=('tot_expenses', 'sum'),
        filing_org=('filing_org', 'first')
    ).reset_index() 

    don = df_schedule_i.groupby(['tax_year','filing_ein']).agg(
        grantee_cash_grant=('grantee_cash_grant', 'sum')).reset_index()

    con = df_contractors.groupby(['tax_year','filing_ein']).agg(
        contractor_amt=('contractor_amt', 'sum')).reset_index()

    pay = df_schedule_j.groupby(['tax_year','filing_ein']).agg(
        total_compensation=('total_compensation', 'sum'),
        total_compensation_filing_org=("total_compensation_filing_org","sum")).reset_index()

    # Merge all yearly data first (before adding totals)

    exp = exp.merge(don,on=['tax_year','filing_ein'],how='left')
    exp = exp.merge(con,on=['tax_year','filing_ein'],how='left')
    exp = exp.merge(pay,on=['tax_year','filing_ein'],how='left')

    # Now calculate totals on the merged data

    totals = exp.groupby(['filing_ein']).agg(
        total_expenses=('total_expenses', 'sum'),
        filing_org=('filing_org', 'first'),
        grantee_cash_grant=('grantee_cash_grant', 'sum'),
        contractor_amt=('contractor_amt', 'sum'),
        total_compensation=('total_compensation', 'sum'),
        total_compensation_filing_org=('total_compensation_filing_org', 'sum')).reset_index()

    totals['tax_year'] = 'Total'
    totals['filing_ein'] = '999999999'

    # Concat totals once

    exp = pd.concat([exp,totals],ignore_index=True)

    df = exp.copy()

    ipi_index = df['filing_org'].unique().tolist().index("ILLINOIS POLICY INSTITUTE")

    filing_org = st.selectbox("Select an IPI Grantee to Follow Their Money",options=df['filing_org'].unique().tolist(),placeholder="ILLINOIS POLICY INSTITUTE",index=ipi_index)

    # Title of Section

    st.markdown(f"""<h1 style="font-family:Arial, Helvetica, sans-serif;">{filing_org}</h1>""", unsafe_allow_html=True)
    
    df_filtered = df[df['filing_org'] == filing_org]

    df_filtered.columns=['Tax Year','Filing Org EIN','Total Expenses','Filing Org','Grants Given','Independent Contractor Expenses','Compensation For Leadership (Filing Org+Related Orgs)','Compensation For Leadership (Filing Org)']
    df_filtered = df_filtered[['Tax Year','Total Expenses','Grants Given','Independent Contractor Expenses','Compensation For Leadership (Filing Org+Related Orgs)','Compensation For Leadership (Filing Org)']]    

    # Create percentages dataframe (out of total expenses)

    df_filtered_perc = df_filtered.copy()
    df_filtered_perc['Grants Given (%)'] = (df_filtered_perc['Grants Given'] / df_filtered_perc['Total Expenses'])
    df_filtered_perc['Independent Contractor Expenses (%)'] = (df_filtered_perc['Independent Contractor Expenses'] / df_filtered_perc['Total Expenses'])
    df_filtered_perc['Compensation For Leadership (Filing Org+Related Orgs) (%)'] = (df_filtered_perc['Compensation For Leadership (Filing Org+Related Orgs)'] / df_filtered_perc['Total Expenses'])
    df_filtered_perc['Compensation For Leadership (Filing Org) (%)'] = (df_filtered_perc['Compensation For Leadership (Filing Org)'] / df_filtered_perc['Total Expenses'])
    
    # select only the percentage columns and Tax Year
    
    df_filtered_perc = df_filtered_perc[['Tax Year','Grants Given (%)','Independent Contractor Expenses (%)','Compensation For Leadership (Filing Org+Related Orgs) (%)','Compensation For Leadership (Filing Org) (%)']]

    # Recreate bar chart, pie chart, and yearly table for total expenses by category

    exp = df_filtered.copy()

    exp_total = exp[exp['Tax Year'] != 'Total']

    exp_total = exp_total[['Total Expenses','Grants Given','Independent Contractor Expenses','Compensation For Leadership (Filing Org)']]

    # Sum all years together for each category
    exp_total_summed = exp_total.sum().reset_index()
    exp_total_summed.columns = ['Expense Category', 'Amount']

    exp_total_perc = df_filtered_perc[df_filtered_perc['Tax Year'] == 'Total']

    exp_total_perc = exp_total_perc[['Tax Year','Grants Given (%)','Independent Contractor Expenses (%)','Compensation For Leadership (Filing Org) (%)']]

    exp_total_perc['Other'] = exp_total_perc['Grants Given (%)'] + exp_total_perc['Independent Contractor Expenses (%)'] + exp_total_perc['Compensation For Leadership (Filing Org) (%)']

    # pivot so "Total" is column name and the rest are values in that column
    exp_total_perc = exp_total_perc.melt(id_vars=['Tax Year'], var_name='Expense Category', value_name='Percentage')

    # get max and min of tax_year

    first_year = df_filtered[df_filtered['Tax Year'] != 'Total']['Tax Year'].min()
    last_year = df_filtered[df_filtered['Tax Year'] != 'Total']['Tax Year'].max()
    first_year = first_year[:4]
    last_year = last_year[:4]

    st.header("Total Expenses Overview")

    st.subheader(f"Total Expenses, Aggregate of All Years {first_year}-{last_year}")

    bar,pie = st.columns(2)
    # Take top 10 for bar chart
    exp_total_summed = exp_total_summed.sort_values(by='Amount',ascending=False).head(10)
    with bar:
        fig = px.bar(exp_total_summed,
            title="Total Expenses by Category",
            x='Expense Category',
            y='Amount',
            labels={'Amount': 'Amount', 'Expense Category': 'Expense Category'},
            height=700,
            text_auto='.2s')
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Amount: $%{y:,.0f}<extra></extra>',
            texttemplate='$%{y:,.0f}',
            textposition='outside',
            textfont_size=20,
            marker=dict(line=dict(color='#000000', width=2)))
        st.plotly_chart(fig, width="stretch")

    with pie:
        fig = px.pie(exp_total_perc,values='Percentage',
        names='Expense Category',
        title='Expense Distribution by Category',
        height=700)
        fig.update_traces(textfont_size=20,
                  marker=dict(line=dict(color='#000000', width=2)))

        st.plotly_chart(fig, width="stretch")

    # By year
    st.subheader(f"Total Expenses by Year, {first_year}-{last_year}")

    data_format = st.radio("Select Format",["$ Amounts","Percentages"])

    if data_format == "$ Amounts":

        st.dataframe(
            df_filtered.style.format({
                'Total Expenses': '${:,.0f}',
                'Grants Given': '${:,.0f}',
                'Independent Contractor Expenses': '${:,.0f}',
                'Compensation For Leadership (Filing Org+Related Orgs)': '${:,.0f}',
                'Compensation For Leadership (Filing Org)': '${:,.0f}'
            }),
            hide_index=True)
    else:
        st.dataframe(
            df_filtered_perc.style.format({
                'Grants Given (%)': '{:.2%}',
                'Independent Contractor Expenses (%)': '{:.2%}',
                'Compensation For Leadership (Filing Org+Related Orgs) (%)': '{:.2%}',
                'Compensation For Leadership (Filing Org) (%)': '{:.2%}'
            }),
            hide_index=True)    

    
    st.header("Schedule I - Grants and Other Assistance to Organizations, Governments, and Individuals")

    # filter for the selected filing org

    st.subheader(f"Grants Awarded, {first_year}-{last_year}")

    # total amount 
    
    df_i_filtered = df_schedule_i[df_schedule_i['filing_org'] == filing_org]

    i_aggregate = df_i_filtered['grantee_cash_grant'].sum()
    i_avg = i_aggregate/(int(last_year)-int(first_year))

    st.markdown(f'''<h2 style="font-size:20px; font-family:Arial, Helvetica, sans-serif;">Total Grants Given by IPI Network: ${i_aggregate:,.2f}</h2>''', unsafe_allow_html=True)
    st.markdown(f'''<h2 style="font-size:20px; font-family:Arial, Helvetica, sans-serif;">Total Grants Given by IPI Network (yearly average): ${i_avg:,.2f}</h2>''', unsafe_allow_html=True)

    

    i_total = df_i_filtered.groupby(['grantee_business_name']).agg(
        grantee_cash_grant=('grantee_cash_grant','sum')
    ).reset_index()

    i_total = i_total.sort_values(by='grantee_cash_grant',ascending=False)

    bar,pie = st.columns(2)

    # Take top 10 for bar chart

    i_total_top_10 = i_total.head(10)

    with bar:

        fig = px.bar(i_total_top_10,
            title="Top 10 Grant Amounts by Grantee Business Name", 
            x='grantee_business_name', 
            y='grantee_cash_grant',
            labels={'grantee_business_name': 'Grantee Business Name', 'grantee_cash_grant': 'Grant Amount'},
            height=600,
            text_auto='.2s')
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Grant Amount: $%{y:,.0f}<extra></extra>',
            texttemplate='$%{y:,.0f}',
            textposition='outside',
            textfont_size=20,
            marker=dict(line=dict(color='#000000', width=2)))
        st.plotly_chart(fig, width="stretch")

    with pie:
        fig = px.pie(i_total,values='grantee_cash_grant',
        names='grantee_business_name',
        title='Grant Distribution by Grantee Business Name',
        height=700)
        fig.update_traces(textfont_size=20,
                  marker=dict(line=dict(color='#000000', width=2)))

        st.plotly_chart(fig, width="stretch")

    st.write(i_total)

    # i_by_year = df_i_filtered.groupby(['tax_year','grantee_business_name']).agg(
    #     grantee_cash_grant_total=('grantee_cash_grant','sum')
    # ).reset_index()


    st.subheader(f"Grants Awarded by Year, {first_year}-{last_year}") 

    st.dataframe(
        i_by_year.style.format({
            'grantee_cash_grant_total': '${:,.0f}'
            }),
        hide_index=True)

    st.header("Part VII-B - Independent Contractors")

    # filter for the selected filing org

    df_viib_filtered = df_contractors[df_contractors['filing_org'] == filing_org]

    # repeat lines 205-245 for df_viib_filtered

    viib_total = df_viib_filtered.groupby(['contractor_name']).agg(
        contractor_amt=('contractor_amt','sum')
    ).reset_index()
    viib_total = viib_total.sort_values(by='contractor_amt',ascending=False)

    st.subheader(f"Independent Contractors by Contractor Name, Aggregate of All Years {first_year}-{last_year}")

    # Take top 10 for bar chart

    viib_total = viib_total.head(10)

    bar,pie = st.columns(2)
    with bar:
        fig = px.bar(viib_total,
            title="Total Independent Contractor Amounts by Contractor Name", 
            x='contractor_name', 
            y='contractor_amt',
            labels={'contractor_name': 'Contractor Name', 'contractor_amt': 'Contractor Amount'},
            height=600,
            text_auto='.2s')
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Contractor Amount: $%{y:,.0f}<extra></extra>',
            texttemplate='$%{y:,.0f}',
            textposition='outside',
            textfont_size=20,
            marker=dict(line=dict(color='#000000', width=2)))
        st.plotly_chart(fig, width="stretch")

    with pie:
        fig = px.pie(viib_total,values='contractor_amt',
        names='contractor_name',
        title='Contractor Distribution by Contractor Name',
        height=700)
        fig.update_traces(textfont_size=20,
                  marker=dict(line=dict(color='#000000', width=2)))
        st.plotly_chart(fig, width="stretch")
    

    viib_by_year = df_viib_filtered.groupby(['tax_year','contractor_name']).agg(
        contractor_amt_total=('contractor_amt','sum')
    ).reset_index()

    st.subheader(f"Independent Contractors by Year, {first_year}-{last_year}")

    st.dataframe(
        viib_by_year.style.format({
            'contractor_amt_total': '${:,.0f}'
            }),
        hide_index=True)

    st.header("Schedule J - Compensation Information for Certain Officers, Directors, Trustees, Key Employees, and Highest Compensated Employees")  

    # filter for the selected filing org and most recent tax year

    j_by_year = df_schedule_j[df_schedule_j['filing_org'] == filing_org]
    # drop duplicates
    j_by_year = j_by_year.drop_duplicates(subset=['compensation_name'])
    df_j_filtered = df_schedule_j[(df_schedule_j['filing_org'] == filing_org) & (df_schedule_j['tax_year'] == "2024-12-31")]
    df_j_filtered = df_j_filtered.drop_duplicates(subset=['compensation_name'])

    j_total = df_j_filtered.copy()

    j_total = j_total.sort_values(by='total_compensation',ascending=False)

    st.subheader(f"Compensation of Highest Paid Employees by Employee Name, 2024")


    bar,pie = st.columns(2)
    with bar:
        fig = px.bar(j_total,
            title="Total Compensation of Highest Paid Employees by Employee Name (2024)", 
            x='compensation_name', 
            y='total_compensation',
            labels={'compensation_name': 'Employee Name', 'total_compensation': 'Total Compensation'},
            height=600,
            text_auto='.2s')
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Total Compensation: $%{y:,.0f}<extra></extra>',
            texttemplate='$%{y:,.0f}',
            textposition='outside',
            textfont_size=20,
            marker=dict(line=dict(color='#000000', width=2)))
        st.plotly_chart(fig, width="stretch")

    with pie:
        fig = px.pie(j_total,values='total_compensation',
        names='compensation_name',
        title='Compensation Distribution of Highest Paid Employees by Employee Name (2024)',
        height=700)
        fig.update_traces(textfont_size=20,
                  marker=dict(line=dict(color='#000000', width=2)))
        st.plotly_chart(fig, width="stretch")

    st.subheader(f"Compensation of Highest Paid Employees by Employee Name and Year, {first_year}-{last_year}")

    j_by_year = j_by_year.sort_values(by='tax_year',ascending=True)

    j_by_year = j_by_year[['tax_year','compensation_name','compensation_title','total_compensation','total_compensation_filing_org']]

    st.dataframe(
        j_by_year.style.format({
            'total_compensation': '${:,.0f}',
            'total_compensation_filing_org': '${:,.0f}'
            }),
        hide_index=True)

    # Show which organizations donate to each

if __name__ == "__main__":
    main()