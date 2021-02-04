document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  document.querySelector('form').onsubmit = () => {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;
    
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });

  }
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load mails in mailbox
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // ... do something else with emails ...
      for (i = 0; i < emails.length; i++) {
        console.log(emails[i]);
        const div = document.createElement('div');
        div.style.display = 'block';
        div.style.border = 'thin solid black';
        div.style.borderBottom = '2px solid black';
        div.style.fontFamily = 'arial';
        

        const senderSpan = document.createElement('span');
        senderSpan.innerHTML = emails[i].sender;
        senderSpan.style.alignSelf = 'baseline';
        senderSpan.style.marginLeft = '5px';
        senderSpan.style.fontWeight = 'bold';
        div.append(senderSpan);

        const subjectSpan = document.createElement('span');
        subjectSpan.innerHTML = emails[i].subject;
        subjectSpan.style.marginLeft = '20px';
        div.append(subjectSpan);

        const timeSpan = document.createElement('span');
        timeSpan.innerHTML = emails[i].timestamp;
        timeSpan.style.color = '#A1A1A1';
        timeSpan.style.float = 'right';
        timeSpan.style.marginRight = '10px';
        div.append(timeSpan);
        
        
        if (emails[i].read === false){
          div.style.backgroundColor = 'white';
        }
        else {
          div.style.backgroundColor = '#eee'
          timeSpan.style.color = 'grey';
        }

        const id = emails[i].id
        div.addEventListener('click', () => load_email(id))
        document.querySelector('#emails-view').append(div);
      }
  });
  }

  function load_email(id) {
    // hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    // delete other emails
    document.querySelector('#email-view').innerHTML = '';
    
    // fetch email
    fetch('/emails/' + id)
    .then(response => response.json())
    .then(email=> {
      // print email
      console.log(email);

      const metaDiv = document.createElement('div');
      metaDiv.style.borderTop = 'thin solid gray';
      metaDiv.style.borderBottom = 'thin solid gray';
      metaDiv.style.marginTop = '10px';
      metaDiv.style.marginBottom = '10px';
      metaDiv.style.paddingTop = '15px';
      metaDiv.style.paddingBottom = '15px';
      
      const fromDiv = document.createElement('div');
      const fromSpan = document.createElement('span');
      fromSpan.innerHTML = 'From: ';
      fromSpan.style.fontWeight = 'bold';
      const fromVar = document.createElement('span');
      fromVar.innerHTML = email.sender;
      fromDiv.append(fromSpan);
      fromDiv.append(fromVar);
      metaDiv.append(fromDiv);
      

      const toDiv = document.createElement('div');
      const toSpan = document.createElement('span');
      toSpan.innerHTML = 'To: ';
      toSpan.style.fontWeight = 'bold';
      const toVar = document.createElement('span');
      toVar.innerHTML = email.recipients;
      toDiv.append(toSpan);
      toDiv.append(toVar);
      metaDiv.append(toDiv);

      const subjectDiv = document.createElement('div');
      const subjectSpan = document.createElement('span');
      subjectSpan.innerHTML = 'Subject: ';
      subjectSpan.style.fontWeight = 'bold';
      const subjectVar = document.createElement('span');
      subjectVar.innerHTML = email.subject;
      subjectDiv.append(subjectSpan);
      subjectDiv.append(subjectVar);
      metaDiv.append(subjectDiv);

      const timeDiv = document.createElement('div');
      const timeSpan = document.createElement('span');
      timeSpan.innerHTML = 'Time: ';
      timeSpan.style.fontWeight = 'bold';
      const timeVar = document.createElement('span');
      timeVar.innerHTML = email.timestamp;
      timeDiv.append(timeSpan);
      timeDiv.append(timeVar);
      metaDiv.append(timeDiv);

      const archive = document.createElement('button');
      archive.classList.add('btn');
      archive.classList.add('btn-primary');
      archive.type = 'button';
      const isArch = email.archived;
      console.log(isArch);
      if (isArch) {
        archive.innerHTML = 'Unarchive';
      }
      else {
        archive.innerHTML = 'Archive';
      }
      archive.addEventListener('click', function() {
        fetch('/emails/' + email.id, {
          method: 'PUT',
          body: JSON.stringify({
            archived: !isArch
          })
        })
        location.href = '';
      })
      metaDiv.append(archive);

    
      const reply = document.createElement('button');
      reply.classList.add('btn');
      reply.classList.add('btn-primary');
      reply.innerHTML = 'Reply'
      reply.type = 'button';
      reply.style.marginLeft = '15px';

      reply.addEventListener('click', function () {
        compose_email();

        document.querySelector('#compose-recipients').value = email.sender;
        if (email.subject.includes('Re:')) {
          document.querySelector('#compose-subject').value = email.subject;
        }
        else {
          document.querySelector('#compose-subject').value = `Re: ${email.subject}` ;
        }
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
      })
      metaDiv.append(reply);

      document.querySelector('#email-view').append(metaDiv);

      const bodyDiv = document.createElement('div');
      bodyDiv.style.marginTop = '15px';
      bodyDiv.innerHTML = email.body;

      document.querySelector('#email-view').append(bodyDiv);

      // mark email as read
      fetch('/emails/' + id, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    })
  }