function deleteNote(noteId){
 fetch('/delete-note',
 { method:'POST',
 body: JSON.stringify({noteId: noteId})
 }).then((_res)=>{
 window.location.href="/teacher-home";
 });
 }
 function deleteUser(userId){
 fetch('/delete-user',
 { method:'POST',
 body: JSON.stringify({userId: userId})
 }).then((_res)=>{
 window.location.href="/admin-board/users";
 });
 }
 function send_data_teacher(courseId){
 fetch('/delete-user',
 { method:'POST',
 body: JSON.stringify({courseId:courseId})
 }).then((_res)=>{
 window.location.href="/admin-board/users";
 });
 }
