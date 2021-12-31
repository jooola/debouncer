import { FunctionComponent } from "react"

import Header from "./components/Header"
import Endpoints from "./components/Endpoints"

const App: FunctionComponent = () => {
  return (
    <div>
      <Header />
      <div className="container-md p-4">
        <Endpoints />
      </div>
    </div>
  )
}

export default App
