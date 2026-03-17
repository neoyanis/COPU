let currentUser = "";
let currentProject = "";

async function register() {
  let email = document.getElementById("email").value;
  let password = document.getElementById("password").value;

  let res = await fetch("/register", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ email, password })
  });

  let data = await res.json();
  alert(JSON.stringify(data));
}

async function login() {
  let email = document.getElementById("email").value;
  let password = document.getElementById("password").value;

  let res = await fetch("/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ email, password })
  });

  let data = await res.json();

  if (data.success) {
    currentUser = email;
    alert("Connecté !");
  } else {
    alert("Erreur login");
  }
}

async function createProject() {
  let name = document.getElementById("projectName").value;

  let res = await fetch("/create-project", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      name,
      email: currentUser
    })
  });

  let data = await res.json();
  currentProject = name;

  alert("Projet créé !");
}

async function save() {
  let code = document.getElementById("code").value;

  await fetch("/save", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      name: currentProject,
      email: currentUser,
      code
    })
  });

  alert("Code sauvegardé !");
}
