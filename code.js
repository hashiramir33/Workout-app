

const API = "https://workout-g2d9fyctefa0bxam.westus3-01.azurewebsites.net";
var login = document.getElementById("lbbuuton");
 login.addEventListener("click", function() {
    window.location.href = `${API}/auth/login`;
    });





 fetch(`${API}/workouts`)
.then(response => response.json())
.then(data => {
    var wol= document.getElementById("workouts")
    var exc= document.getElementById("exc")
    var set = document.getElementById("sets")
    var reps = document.getElementById("reps")
    var weight = document.getElementById("weight")
    var form = document.getElementById("workoutForm")
    var welcome = document.getElementById("welcome");
    var login = document.getElementById("lbbuuton");
    var logout = document.getElementById("logouttbbutt");

   

  logout.addEventListener("click", function() {
    fetch(`${API}/auth/logout`, {
        credentials: "include"
    })
    .then(() => {
        location.reload();
    });
});



     fetch(`${API}/api/user`, {
    credentials: "include"
     })
    .then(response => response.json())
    .then(user => {

    if (user.logged_in) {
            welcome.textContent = "Hello, " + user.name + "!";
            login.hidden = true;
            logout.hidden = false;
    } 
    
    else {
            welcome.textContent = "";
            login.hidden = false;
            logout.hidden = true;
    }

    });




   






    for(var i = 0; i < data.length; i++){

        var li = document.createElement("li");
        li.textContent =data[i].Excer + " - " +
                        data[i].setsss + " sets - " +
                        data[i].Reps + " reps - " +
        
                        data[i].Weight + " lbs";

                        wol.appendChild(li)



    }

    form.addEventListener("submit", function(event){
        event.preventDefault()
        var ex=exc.value
        var exs=Number(set.value)
        var re = Number(reps.value)
        var wevalue= Number(weight.value)
        if(ex===""|| ex.length>30){
            alert("Excersize name should be less han 50")
            return;
        }
        if(exs<=0|| re<=0 || wevalue<=0){
            alert("value has to be positive")
            return;

        }








        var work={
            Excer: ex,
            setsss: exs,
            Reps: re,
            Weight: wevalue

        }
       fetch(`${API}/workouts`,{
           method : "POST",
           headers: {
            "Content-Type": "application/json"
           },
           body: JSON.stringify(work)
        })
        .then(response=> response.json())
        .then(data => {
            location.reload()
          


    })

    




    
})

var cb= document.getElementById("cb")

cb.addEventListener("click", function(){
    fetch(`${API}/workouts`, {
           method : "DELETE"
    })
    .then(response=> response.json())
    .then(data => {
            location.reload()
          


    })

})
})
