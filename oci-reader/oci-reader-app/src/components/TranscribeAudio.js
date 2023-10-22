import React from 'react'
import { Card, Typography } from "@material-tailwind/react";
import { LoaderComp } from './loader';

export const TranscribeAudio = () => {

  const [loading, setLoading] = React.useState(false);
  const [dataTable, setTable] = React.useState([])

  React.useEffect(() => {
    getData()
  }, [])

  const getData = async () => {
    setLoading(true)
    console.log("Loading data...");
    const data = await fetch('api-reader')
      .catch((err) => {
        console.log(err);
      })
      .finally(() => {
        setLoading(false);
      });

    const transcribeData = []
    try{
      console.info("Loading info ...")
      const transcribeData = await data.json()
      
      try{
        //try to get OCI error
        if (transcribeData.data.includes('error')) {
          console.log(transcribeData.data);
        }
      }catch(error){ 
        console.error("Error")
        console.error(error)
      }
      console.log(transcribeData)
      setTable(transcribeData)
    }catch(error){     
      console.error(error)      
    }

  }


  const DisplayData = dataTable.map(
    (info, index) => {
      return (
        <tr key={index} className="even:bg-blue-gray-50/50">
          <td className='p-4'><Typography
            variant="small"
            color="blue-gray"
            className="font-normal">{info.id}</Typography>
          </td>
          <td className='p-4 h-full w-full' ><Typography
            variant="small"
            color="blue-gray"
            className="font-normal">{info.text}</Typography>
          </td>
          <td className='p-4'><Typography
            variant="small"
            color="blue-gray"
            className="font-normal">{info.confidence}</Typography>
          </td>
        </tr>
      )
    }
  )

  const table = <Card className="container h-full w-full overflow-scroll">
    <table className="table-auto text-left">
      <thead>
        <tr>
          <th>
            <Typography
              variant="small"
              color="blue-gray"
              className="border-b border-blue-gray-100 bg-blue-gray-50 p-4">Id</Typography>
          </th>
          <th>
            <Typography
              variant="small"
              color="blue-gray"
              className="border-b border-blue-gray-100 bg-blue-gray-50 p-4">Text</Typography>
          </th>
          <th>
            <Typography
              variant="small"
              color="blue-gray"
              className="border-b border-blue-gray-100 bg-blue-gray-50 p-4">Confidence</Typography>
          </th>
        </tr>
      </thead>
      <tbody>
        {DisplayData}
      </tbody>
    </table>
  </Card>


  if (loading) {
    return (
      <LoaderComp />)
  }

  return (table)
}
