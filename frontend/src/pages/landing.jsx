import { useEffect, useState } from "react"

const Landing = () => {
    
    const [data, setData] = useState("")

    useEffect(() => {
        fetch(process.env.REACT_APP_BACKEND_URL + "/api/test")
            .then((res) => res.json())
            .then((data) => setData(data.data))
    }, [])

    return (
        <div className="landing">
           <p>Woooaaaah, what a cool landing page! :o</p>
           <p>{data}</p>
        </div>
    )

}

export default Landing