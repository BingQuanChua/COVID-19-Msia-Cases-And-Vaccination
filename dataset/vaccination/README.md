# Documentation for AEFI datasets
An adverse event following immunisation (AEFI) is any untoward medical occurrence which follows immunisation. AEFIs are not necessarily caused by the vaccine - they can be related to the vaccine itself, to the vaccination process (stress related reactions) or can occur independently from vaccination (coincidental). 

The datasets include cases reported through both the NPRA Reporting System and MySejahtera.


_Disclaimers:_ 
- _The data are unverified (i.e. self-declared) reports of adverse events, both minor and serious, that occur after immunisation._
- _The number of reports alone cannot used to reach conclusions about the existence, severity, frequency, or rates of AEFIs associated with vaccines._
- _Reported events are not always proven to have a causal relationship with the vaccine. Establishing causality requires additional investigation. Serious AEFI reports are always followed-up and investigated thoroughly for better understanding of the circumstances. However, our public data does not generally change based on information obtained from the investigation process (i.e. we do not reduce AEFI counts after the fact)._
- _The NPRA and MOH always consider the complexities mentioned above, in addition to various other factors, when analysing and monitoring vaccine safety._


## Variables and Methodology

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date



# Documentation for vaccination datasets

## File naming convention

1) `vax_malaysia.csv`: Static name; file is updated by 0200hrs daily
2) `vax_state.csv`: Static name; file is updated by 0200hrs daily

## Variables

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date
2) `state`: Name of state (present in state file, but not country file)
3) `daily_partial`: 1st doses (for double-dose vaccines) delivered between 0000 and 2359 on date
4) `daily_full`: 2nd doses (for single-dose vaccines) and 1-dose vaccines (e.g. Cansino) delivered between 0000 and 2359 on date.
5) `daily` = `daily_partial` + `daily_full`
6) `cumul_partial` = sum of `daily_partial` + `cansino` for all T <= `date`
7) `cumul_full` = sum of `daily_full` for all T <= `date`
8) `cumul_partial_child` = number of children (< 18yo) who have received their 1st dose (thus far, only Pfizer is used)
9) `cumul_full_child` = number of children (< 18yo)  who have received their 2nd dose (thus far, only Pfizer is used)
10) `cumul` = `cumul_partial` + `cumul_full` - cumulative `cansino` doses to date
11) `x1`and `x2` = 1st and 2nd doses of double-dose vaccine type `x` delivered between 0000 and 2359 on date, where `x` can be `pfizer`, `sinovac` or `astra`
12) `x` = doses of single-dose vaccine type `x` delivered between 0000 and 2359 on date, where `x` can be `cansino`
13) `pending` = doses delivered that are 'quarantined' in the Vaccine Management System due to errors and/or inconsistencies in vaccine bar code, batch number, et cetera; these problems are usually resolved soon and affect ~0.1% of all records on a rolling basis. `pending` records for dates far in the past are not unresolved errors, but rather reflect backdated manual uploads.

## Methodological choices
+ The variable `cumul` shows the number of `unique` doses which have been administered. However, people are also interested in tracking the number of _unique individuals_ who have been vaccinated - this is captured by the variable `cumul_partial`, which compromises people who received 1 dose of a double-dose vaccine, and those who received a single-dose vaccine.  `cumul_full` is a perfect subset of `cumul_partial` - individuals who received a single-dose vaccine are also included here. This is why `cumul` does not equal `cumul_partial` + `cumul_full` - the number of single-dose vaccines administered must be deducted.
+ With substantial outreach efforts in areas with poor internet access, vaccinations (which are normally tracked in real time) have to be documented offline (think Excel sheets and paper forms). Given that outreach programs may last days at a time, records of these vaccinations may only be uploaded and consolidated a few days after the day on which they occured. Consequently, we may revise the dataset from time to time if more data is reported for dates already contained within the datasets. These revisions will typically cause vaccination counts to increase, though minor decreases may be observed if there are corrections to dosage dates after they are recorded and published under another day's data. Thus far, revsisions have been made on:
     + [17th July](https://github.com/CITF-Malaysia/citf-public/commit/2f3100bce891e34c660471ac4dc96dddb911e6eb#diff-61b43ea1f6043e3ce51f4264320ef8907ad059425fc3bcf7cc9f4c20fac3b025)
     + [25th July](https://github.com/CITF-Malaysia/citf-public/commit/1e49d7268e546c325e83fbd9ce4ca0b3c1186756#diff-61b43ea1f6043e3ce51f4264320ef8907ad059425fc3bcf7cc9f4c20fac3b025)
     + [1st August](https://github.com/CITF-Malaysia/citf-public/commit/14c8ab854257e369b6a43f9b7ae97f58c92cef42#diff-61b43ea1f6043e3ce51f4264320ef8907ad059425fc3bcf7cc9f4c20fac3b025) - also reflecting integration of SelVAX transactions
     + [8th August](https://github.com/CITF-Malaysia/citf-public/commit/8f6b68885e82a99de6040acb1cf33adafd360c64#diff-61b43ea1f6043e3ce51f4264320ef8907ad059425fc3bcf7cc9f4c20fac3b025)
     + [15th August](https://github.com/CITF-Malaysia/citf-public/commit/f9206aed251613c3492f7b9fa01bd8aaffd2c9d5)
     + [23rd August](https://github.com/CITF-Malaysia/citf-public/commit/238abf321bf0095cdf95f27e142e2603fe99861a)
     + [30th August](https://github.com/CITF-Malaysia/citf-public/commit/693ba64fd8c4f83a0869c1b03a5605f9e3755d2b)
