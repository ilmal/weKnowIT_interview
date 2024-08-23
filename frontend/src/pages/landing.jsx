import { useEffect, useState } from "react"
import  { Link } from 'react-router-dom'

const Landing = () => {
    const [stories, setStories] = useState([])
    const [generated_stories, setGenerated_stories] = useState([])

    useEffect(() => {
        const requestOptions = {
            method: 'GET',
        };
        fetch(process.env.REACT_APP_BACKEND_URL + "/api/get_stories", requestOptions)
            .then(response => response.json())
            .then(data => {
                console.log("IMPORTED: ", data)
                setStories(data)
            })
        
        fetch(process.env.REACT_APP_BACKEND_URL + "/api/get_generated_stories", requestOptions)
            .then(response => response.json())
            .then(data => {
                console.log("GENERATED: ", data)
                setGenerated_stories(data)
            })

    }, [])

    const list_stories = (type) => {
        const stories_arr = []
        const active_array = type === "generated"? generated_stories: stories

        active_array.forEach(element => {
            stories_arr.push(
                <Link to={`/${type === "generated"?"story_generated":"story"}?story=${element[1]}`} key={element} style={{}}>{element[1]}</Link>
            )
        });
  
        return stories_arr
    }

    return (
        <>
            <div className="home">
                <div className="title">
                    <p>
                        Available stories
                    </p>
                </div>
                <div className="story_lists">
                    <div className="imported_stories story_list">
                        {
                            stories.length === 0 ?  
                            <p className="loading_message">
                                Loading stories...
                            </p>                        
                            : 
                            <>
                                <h1>Imported Stories</h1>
                                {list_stories("imported")}      
                            </>
                        }
                    </div>
                    <div className="generated_stories story_list">
                        {
                            stories.length === 0 ?  
                            <p className="loading_message">
                                Loading stories...
                            </p>                        
                            : 
                            <>
                                <h1>Generated Stories</h1>
                                {list_stories("generated")}      
                            </>                        
                        }
                    </div>
                </div>
            </div>
        </>
    )

}

export default Landing