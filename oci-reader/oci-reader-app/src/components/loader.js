import React from 'react'
import { Circles } from "react-loader-spinner";

export const LoaderComp = () => {
    return (
        <Circles
            height="80"
            width="80"
            color="#4fa94d"
            ariaLabel="circles-loading"
            wrapperStyle={{}}
            wrapperClass="center_spinner"
            visible={true}
        />
    )
}

