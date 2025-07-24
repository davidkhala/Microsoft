# Invite another admin
[source](https://learn.microsoft.com/en-us/answers/questions/1432095/how-do-i-add-a-user-to-be-an-administrator-in-my-a)
1. Log into the [Microsoft Entra admin center](https://entra.microsoft.com) as a User Administrator.
2. `Identity` > `Users` > All users > New user > Invite external user.
3. Fill in the user's identity details and set the User type as either Member or Guest.
4. Assign the new user to Microsoft Entra roles
  - In `Manage/Assigned roles` of left pane, Click `+ Add assignments`
  - `Global Administrator` is the root role
5. click the Invite button to send an email invitation. This adds the user account to the directory as a guest.
  - If the user hasn't accepted the invitation, go to Identity > Users > All users, select the invited user, and check the invitation state under the B2B collaboration tile. You can resend the invitation if needed
