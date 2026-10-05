fetch("http://127.0.0.1:5000/workouts")
.then(response => response.json())
.then(data => {
    var wol= document.getElementById("workouts")
    var exc= document.getElementById("exc")
    var set = document.getElementById("sets")
    var reps = document.getElementById("reps")
    var weight = document.getElementById("weight")
    var form = document.getElementById("workoutForm")

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
        var work={
            Excer: exc.value,
            setsss: set.value,
            Reps: reps.value,
            Weight: weight.value

        }
        fetch("http://127.0.0.1:5000/workouts",{
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
    fetch("http://127.0.0.1:5000/workouts",{
           method : "DELETE"
    })
    .then(response=> response.json())
    .then(data => {
            location.reload()
          


    })

})
})