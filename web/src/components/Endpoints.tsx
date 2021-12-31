import { FunctionComponent, useEffect, useState } from "react"
import Form from "react-bootstrap/Form"
import Button from "react-bootstrap/Button"
import Table from "react-bootstrap/Table"
import { useForm } from "react-hook-form"

import { EndpointsAPI, Endpoint } from "../api"

const Endpoints: FunctionComponent = () => {
  const [endpoints, setEndpoints] = useState<Array<Endpoint>>([])

  const hydrate = async () => {
    const response = await EndpointsAPI.list()
    const payload = await response.json()
    setEndpoints(payload)
  }

  const { register, watch } = useForm<Endpoint>({
    defaultValues: {
      url: "https://example.com/",
      method: "POST",
      timeout: 10,
    },
  })

  const createEndpoint = async () => {
    const response = await EndpointsAPI.create(watch())
    console.log(response)
    await hydrate()
  }

  const deleteEndpoint = (uid: string) => {
    return async () => {
      const response = await EndpointsAPI.delete(uid)
      console.log(response)
      await hydrate()
    }
  }

  useEffect(() => {
    hydrate()
  }, [])

  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th style={{ width: "22rem" }}>ID</th>
          <th style={{ width: "8rem" }}>Method</th>
          <th>URL</th>
          <th style={{ width: "6rem" }}>Timeout</th>
          <th style={{ width: "6rem" }}></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td></td>
          <td className="p-1">
            <Form.Select size="sm" {...register("method")}>
              <option value="POST">POST</option>
              <option value="GET">GET</option>
            </Form.Select>
          </td>
          <td className="p-1">
            <Form.Control size="sm" type="text" {...register("url")} />
          </td>
          <td className="p-1">
            <Form.Control size="sm" type="number" {...register("timeout")} />
          </td>
          <td className="p-1">
            <Button variant="success" size="sm" onClick={createEndpoint}>
              Create
            </Button>
          </td>
        </tr>
        {endpoints.map((endpoint) => (
          <tr key={endpoint.uid}>
            <td>{endpoint.uid}</td>
            <td>{endpoint.method}</td>
            <td>{endpoint.url}</td>
            <td>{endpoint.timeout}</td>
            <td className="p-1">
              <Button
                variant="danger"
                size="sm"
                onClick={deleteEndpoint(endpoint.uid)}
              >
                Delete
              </Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  )
}

export default Endpoints
