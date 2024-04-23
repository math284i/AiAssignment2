using AiAssignment2;

Console.WriteLine("Hello, World!");

//Forestil dig du starter med og tro på noget som, jorden er flad. Så får du at vide at hvis jorden er flad,
//så kan du se bjerge fra dit vindue. Du lærer så senere at man ikke kan se bjerge fra dit vindue, så nu skal vi fjerne
//den fra vores belief base, og opdatere de andre ting der er relateret til vores nye information. 


//design and implementation of belief base
//Måske bruge et hashtable eller hashset

//Når man får ny information, skal man gennemgå alt information vi allerede kender

var engine = new Engine();

engine.BeliefBase.Add("A");
engine.BeliefBase.Add("B");
if (engine.BeliefBase.Contains("A"))
{
    engine.BeliefBase.Remove("A");
}

foreach (var belief in engine.BeliefBase)
{
    Console.WriteLine(belief);
}








