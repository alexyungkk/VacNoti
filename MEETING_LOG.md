# VacNoti Project - Client Consultation & Meeting Logs

This document tracks the iterative design, requirements gathering, and software quality assurance (QA) cycles conducted with the hotel supervisor (end-user/client) during the development of the VacNoti application.

### Meeting Log: Client Consultation & Requirements Gathering

**Date:** May 1, 2026  
**Participant:** Supervisor (Client / End-User)

#### Purpose of the Meeting:

To understand the current manual workflow for daily room assignments and gather software requirements for the web application.

#### Observations of Current Workflow:

1. Every morning, the supervisor manually manages hotel room assignments using a master Excel template.
2. The assignment process is completely manual: the supervisor looks at the available staff and typed each specific room number directly into individual columns designated for each room attendant.
3. This repetitive manual input is time-consuming and prone to human data-entry errors.

#### Software Opportunities Identified:

- **Automation:** The application should read an uploaded schedule and process assignment connections automatically, eliminating the need to type numbers cell-by-cell manually.
- **Notification System:** Once assignments are processed, the supervisor needs a fast, centralized method to instantly notify attendants on the floor about room status updates (Vacant/Stayover).

#### Next Steps:

- Design an initial Excel schedule template that mirrors the hotel's operational columns (`Sched`, `roomList`, `roomNum`) to test data parsing logic in Python.

### Meeting Log: Format Alignment & Feature Expansion

**Date:** May 4, 2026  
**Participant:** Supervisor (Client / End-User)

#### Purpose of the Meeting:

To review the structural format of the supervisor's operational Excel file and discuss necessary feature enhancements for the application's reporting capabilities.

#### Feedback & New Requirements Gathered:

1. **Excel Format Alignment:** The supervisor shared the specific column layouts and structure of his daily spreadsheet. To match his existing system perfectly, the application requires an additional workbook page dedicated strictly to room number inputs.
2. **Feature Expansion (Stayover Option):** In addition to tracking check-outs, the supervisor requested a new workflow toggle to send distinct "Stayover" service notifications to attendants on the floor.
3. **Data Retention (Message History Log):** The supervisor requested a visual history log directly inside the application interface to review sent messages and track historical notification data throughout the shift.

#### Engineering & Design Changes Implemented:

- **UI Redesign:** Added an interactive radio-button toggle to switch the alert context between `Check out` and `Stayover` seamlessly.
- **Database / State Management:** Set up a local data logging mechanism (`simple.json`) to act as a persistent file storage solution, ensuring message history remains intact even if the application refreshes.
- **Excel Logic Restructuring:** Modified the template generation script to map perfectly to the required multi-page layout (`Sched` page and `roomList` page).

#### Next Steps:

- Build and integrate the persistent message history view in the Streamlit user interface using a JSON backend.
- Test the notification dispatch conditional logic for both room states.

### Meeting Log: Integration Testing, Issue Diagnosis & Feature Refinement

**Date:** May 26, 2026  
**Participant:** Supervisor (Client / End-User)

#### Purpose of the Meeting:

To conduct user acceptance testing (UAT) with the updated application prototype, review the compatibility of the generated Excel template on the client's local workstation, and add testing safeguards.

#### Key Issues Identified & Diagnosed:

1. **Client Environment Compatibility Conflict:** During live testing on the supervisor's workstation, the Excel calculation engine failed to automatically update the dependent formulas on the `roomList` sheet upon data insertion.
2. **Root Cause Analysis:** The issue was diagnosed as an environment configuration mismatch. The supervisor's host Microsoft Excel application defaults to _Manual Calculation mode_ for corporate workflow compliance. Because the original Excel template didn't explicitly instruct the workbook to auto-calculate, the client environment suppressed the execution of the sheet's internal cell logic.
3. **SMS Verification Safeguard Needed:** While testing the validation paths, a requirement was identified to decouple the application logic from the live cellular gateway. The supervisor needed a way to thoroughly stress-test the UI inputs without broadcasting live SMS alerts to staff or consuming Twilio API credits.

#### Engineering Resolutions & Feature Implementations:

- **Environment Workaround Protocol:** Established a defensive deployment plan to manually switch the workstation calculation configuration during the operational demonstration, ensuring zero impact on other corporate files.
- **QA Dry-Run Feature Configuration:** Programmed a conditional logic gate controlled by a new interactive boolean checkbox component in the Streamlit UI.
  - **Checked (True):** Executes the full operational cycle including the background Twilio API client broadcast.
  - **Unchecked (False):** Runs data validations, processes state mutations, updates the `simple.json` historical tracker, and updates the logger UI while explicitly bypassing the cellular carrier submission path.

#### Next Steps:

- Stage the codebase changes in VS Code, execute final local verification test cases, and commit the feature branch up to GitHub.
- Coordinate the final deployment review session.

---

### Meeting Log: Scope Expansion & Dynamic Notification Routing

**Date:** June 3, 2026  
**Participant:** Supervisor (Client / End-User)

#### Purpose of the Meeting:

To discuss a new operational requirement for processing real-time guest requests and map out the frontend inputs needed for the application.

#### New Requirements Gathered:

1. **Special Requests Integration:** The supervisor requested a new function to handle ad-hoc guest requirements that occur dynamically throughout the shift (e.g., delivering slippers, extra towels, or blankets).
2. **Targeted SMS Dispatch:** The feature must allow the supervisor to select or input a specific room number, type out the custom guest requirement, and instantly route that custom text message straight to the assigned room attendant's mobile device.

#### Technical & UI Architecture Plan:

- **UI Input Fields:** Implement a dynamic text area component (`st.text_area` or `st.text_input`) in the Streamlit interface to capture free-form text for custom guest requirements.
- **Data Validation & Logic Routing:** Code a verification check to ensure the custom message is not empty before submission, then reuse the existing Twilio API gateway logic to securely compile and transmit the specific text package string.

#### Next Steps:

- Add the new user interface elements in `VacNoti.py` to handle custom text inputs.
- Update the conditional block to format the custom SMS string nicely (e.g., _"From Supervisor: Room [X] requires [Special Request], thank you."_).
- Test the input text length validations to prevent empty or broken SMS dispatches.
