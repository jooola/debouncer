const API = new URL(
    "/api",
    import.meta.env.PROD ? window.location.origin : "http://localhost:4000"
)

export interface Call {
    status: string
    redispatch: boolean
}

export interface Endpoint {
    uid: string
    url: string
    method: string
    timeout: number
    call?: Call
}

export class EndpointsAPI {
    static list() {
        return fetch(`${API}/`)
    }

    static create(body: { url: string; method: string; timeout: number }) {
        return fetch(`${API}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        })
    }

    static delete(uid: string) {
        return fetch(`${API}/${uid}`, { method: "DELETE" })
    }
}
