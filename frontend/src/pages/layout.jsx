import { Outlet, Link } from "react-router-dom";
import { useEffect, useState } from "react";

const Layout = () => {

    console.log()

    return (
        <>
            <div className="header">
                <div className="pages">
                    <Link to="/">
                        <p>Home</p>
                    </Link>
                    <Link to={"/" + Math.random().toString().substring(2)}>
                        <p>Random</p>
                    </Link>
                </div>
            </div>
            <Outlet />
            <div className="footer">
                <p onClick={()=>window.scrollTo(0, 0)}>Back to top</p>
            </div>
        </>
    )

}

export default Layout