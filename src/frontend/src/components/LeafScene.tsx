import { Environment, Float } from '@react-three/drei'
import { Canvas } from '@react-three/fiber'
import { Suspense } from 'react'
import LeafModel from './LeafModel'

type Props = {
  loading?: boolean
}

export default function LeafScene({ loading = false }: Props) {
  return (
    <div className={`leaf-scene ${loading ? 'is-loading' : ''}`}>
      <Canvas
        dpr={[1, 2]}
        gl={{ alpha: true, antialias: true }}
        camera={{ position: [0, 0, 3], fov: 30 }}
      >
        <ambientLight intensity={1.55} />
        <hemisphereLight intensity={0.95} groundColor="#d9e7dc" />
        <directionalLight position={[2.4, 2.8, 3]} intensity={1.7} />
        <directionalLight position={[-1.8, -1.1, 2]} intensity={0.55} />
        <pointLight
          position={[0, 0.4, 1.8]}
          intensity={loading ? 0.85 : 0.45}
          distance={5}
        />

        <Suspense fallback={null}>
          <Float
            speed={loading ? 1.55 : 0.95}
            rotationIntensity={loading ? 0.14 : 0.08}
            floatIntensity={loading ? 0.14 : 0.08}
          >
            <LeafModel loading={loading} />
          </Float>

          <Environment preset="studio" />
        </Suspense>
      </Canvas>
    </div>
  )
}