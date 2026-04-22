import { useEffect, useRef, useState } from 'react'
import { MapContainer, TileLayer, GeoJSON } from 'react-leaflet'
import L from 'leaflet'
import api from '../services/api'
import { useAuth } from '../context/AuthContext'

function MapView() {
  const { logout } = useAuth()

  const [wilayah, setWilayah] = useState(null)
  const [fasilitas, setFasilitas] = useState(null)

  const [formMode, setFormMode] = useState('add')
  const [selectedId, setSelectedId] = useState(null)

  const [nama, setNama] = useState('')
  const [jenis, setJenis] = useState('')
  const [alamat, setAlamat] = useState('')
  const [longitude, setLongitude] = useState('')
  const [latitude, setLatitude] = useState('')

  const geoJsonRef = useRef(null)
  const mapRef = useRef(null)

  const loadWilayah = async () => {
    const res = await api.get('/api/wilayah/geojson')
    setWilayah(res.data)
  }

  const loadFasilitas = async () => {
    const res = await api.get('/api/fasilitas/geojson')
    setFasilitas(res.data)
  }

  useEffect(() => {
    loadWilayah()
    loadFasilitas()
  }, [])

  useEffect(() => {
    if (wilayah && geoJsonRef.current && mapRef.current) {
      const bounds = geoJsonRef.current.getBounds()
      mapRef.current.fitBounds(bounds, { padding: [20, 20] })
    }
  }, [wilayah])

  const resetForm = () => {
    setFormMode('add')
    setSelectedId(null)
    setNama('')
    setJenis('')
    setAlamat('')
    setLongitude('')
    setLatitude('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const payload = {
      nama,
      jenis,
      alamat,
      longitude: parseFloat(longitude),
      latitude: parseFloat(latitude)
    }

    try {
      if (formMode === 'add') {
        await api.post('/api/fasilitas', payload)
      } else {
        await api.put(`/api/fasilitas/${selectedId}`, payload)
      }

      await loadFasilitas()
      resetForm()
      alert('Data berhasil disimpan')
    } catch (error) {
      alert(error.response?.data?.detail || 'Gagal menyimpan data')
    }
  }

  const handleDelete = async (id) => {
    const confirmDelete = window.confirm('Yakin ingin menghapus data ini?')
    if (!confirmDelete) return

    try {
      await api.delete(`/api/fasilitas/${id}`)
      await loadFasilitas()
      resetForm()
      alert('Data berhasil dihapus')
    } catch (error) {
      alert(error.response?.data?.detail || 'Gagal menghapus data')
    }
  }

  const handleEdit = async (id) => {
    try {
      const res = await api.get(`/api/fasilitas/${id}`)
      const data = res.data

      setFormMode('edit')
      setSelectedId(id)
      setNama(data.nama)
      setJenis(data.jenis)
      setAlamat(data.alamat)
      setLongitude(data.lon)
      setLatitude(data.lat)
    } catch (error) {
      alert('Gagal mengambil data edit')
    }
  }

  const styleWilayah = () => ({
    color: '#ff0000',
    weight: 2,
    fillColor: '#ff9999',
    fillOpacity: 0.3
  })

  const pointToLayer = (feature, latlng) => {
    return L.marker(latlng)
  }

  useEffect(() => {
    window.editFasilitas = handleEdit
    window.deleteFasilitas = handleDelete

    return () => {
      delete window.editFasilitas
      delete window.deleteFasilitas
    }
  }, [fasilitas])

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div style={{ width: '320px', padding: '16px', background: '#f8f9fa', overflowY: 'auto' }}>
        <h2>WebGIS Tugas 9</h2>
        <p><b>Muharyan Syaifullah</b></p>
        <p>123140045</p>

        <button onClick={logout} style={{ marginBottom: '16px' }}>
          Logout
        </button>

        <h3>{formMode === 'add' ? 'Tambah Fasilitas' : 'Edit Fasilitas'}</h3>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <input
            type="text"
            placeholder="Nama"
            value={nama}
            onChange={(e) => setNama(e.target.value)}
            required
          />

          <input
            type="text"
            placeholder="Jenis"
            value={jenis}
            onChange={(e) => setJenis(e.target.value)}
            required
          />

          <textarea
            placeholder="Alamat"
            value={alamat}
            onChange={(e) => setAlamat(e.target.value)}
            required
          />

          <input
            type="number"
            step="any"
            placeholder="Longitude"
            value={longitude}
            onChange={(e) => setLongitude(e.target.value)}
            required
          />

          <input
            type="number"
            step="any"
            placeholder="Latitude"
            value={latitude}
            onChange={(e) => setLatitude(e.target.value)}
            required
          />

          <button type="submit">
            {formMode === 'add' ? 'Tambah' : 'Update'}
          </button>

          {formMode === 'edit' && (
            <button type="button" onClick={resetForm}>
              Batal Edit
            </button>
          )}
        </form>
      </div>

      <div style={{ flex: 1 }}>
        <MapContainer
          center={[-6.33, 106.81]}
          zoom={11}
          style={{ height: '100%', width: '100%' }}
          ref={mapRef}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="&copy; OpenStreetMap contributors"
          />

          {wilayah && (
            <GeoJSON
              ref={geoJsonRef}
              data={wilayah}
              style={styleWilayah}
              onEachFeature={(feature, layer) => {
                layer.bindPopup(`
                  <div>
                    <h3>${feature.properties.nama}</h3>
                    <p><b>ID:</b> ${feature.properties.id}</p>
                  </div>
                `)
              }}
            />
          )}

          {fasilitas && (
            <GeoJSON
              data={fasilitas}
              pointToLayer={pointToLayer}
              onEachFeature={(feature, layer) => {
                const props = feature.properties

                layer.bindPopup(`
                  <div>
                    <h3>${props.nama}</h3>
                    <p><b>Jenis:</b> ${props.jenis ?? '-'}</p>
                    <p><b>Alamat:</b> ${props.alamat ?? '-'}</p>
                    <button onclick="window.editFasilitas(${props.id})">Edit</button>
                    <button onclick="window.deleteFasilitas(${props.id})">Delete</button>
                  </div>
                `)
              }}
            />
          )}
        </MapContainer>
      </div>
    </div>
  )
}

export default MapView