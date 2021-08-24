import React, { useState, createContext } from 'react'


export const UserRegContext = createContext();

export const UserContextProvider = (props) => {
    const [userDetail, setUserDetail] = useState({
        username: "",
        email: "",
        password: ""
    })

    return (
        <UserRegContext.Provider value={[userDetail, setUserDetail]}>
            {props.children}
        </UserRegContext.Provider>
    )
}