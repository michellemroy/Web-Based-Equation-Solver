obj = {
    eq1 : null,

    //eq1 : "hello",
    
    eq2 : null ,

    //eq2 : "hello",

    xhr : new XMLHttpRequest(),

    checkEqs : function(event)
    {
        //alert(obj.eq1.value);
        if(obj.eq1.value.length > 2 && obj.eq2.value.length > 2)
            return true;
        return false;
    },

    sendEqs : function()
    {
        if(obj.checkEqs())
        {
            obj.xhr.open("GET","localhost:5000/solveEq?eq1=hello",true);
            obj.xhr.onreadystatechange = obj.dispSoln;
            obj.xhr.send();

        }
    },

    dispSoln : function()
    {
        if(obj.xhr.readyState == 4 && obj.xhr.status == 200)
        {
            resp = JSON.parse(obj.xhr.responseText);
            x = resp.x;
            y = resp.y;

            alert("X : "+x+"Y : "+y);
        }
    },

    init: function()
    {
        obj.eq1 = document.getElementById("eq1");
        obj.eq2 = document.getElementById("eq2");

    }


}

