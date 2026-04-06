import { Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { Environment, Float } from '@react-three/drei'
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
        camera={{ position: [0, 0.15, 3.2], fov: 32 }}
      >
        <ambientLight intensity={1.9} />
        <hemisphereLight intensity={0.9} groundColor="#d9e7dc" />
        <directionalLight position={[2.5, 2.5, 3]} intensity={1.8} />
        <directionalLight position={[-2, -1.5, 2]} intensity={0.7} />

        <Suspense fallback={null}>
          <Float
            speed={loading ? 2.2 : 1.3}
            rotationIntensity={loading ? 0.35 : 0.18}
            floatIntensity={loading ? 0.5 : 0.28}
          >
            <LeafModel />
          </Float>

          <Environment preset="studio" />
        </Suspense>
      </Canvas>
    </div>
  )
}