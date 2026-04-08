import { Environment, Float } from '@react-three/drei'
import { Canvas } from '@react-three/fiber'
import { Suspense } from 'react'
import LeafModel from './LeafModel'

type Props = {
  loading?: boolean
  variant?: 'default' | 'auth'
}

export default function LeafScene({
  loading = false,
  variant = 'default',
}: Props) {
  const isAuth = variant === 'auth'

  return (
    <div className={`leaf-scene ${loading ? 'is-loading' : ''} ${isAuth ? 'is-auth' : ''}`}>
      <Canvas
        dpr={[1, 2]}
        gl={{ alpha: true, antialias: true }}
        camera={{
          position: isAuth ? [0, 0, 3.4] : [0, 0, 3],
          fov: isAuth ? 32 : 30,
        }}
      >
        <ambientLight intensity={isAuth ? 1.35 : 1.55} />
        <hemisphereLight intensity={isAuth ? 0.82 : 0.95} groundColor="#d9e7dc" />
        <directionalLight position={[2.4, 2.8, 3]} intensity={isAuth ? 1.45 : 1.7} />
        <directionalLight position={[-1.8, -1.1, 2]} intensity={isAuth ? 0.42 : 0.55} />
        <pointLight
          position={[0, 0.4, 1.8]}
          intensity={loading ? 0.85 : isAuth ? 0.28 : 0.45}
          distance={5}
        />

        <Suspense fallback={null}>
          <Float
            speed={isAuth ? 0.75 : loading ? 1.55 : 0.95}
            rotationIntensity={isAuth ? 0.04 : loading ? 0.14 : 0.08}
            floatIntensity={isAuth ? 0.03 : loading ? 0.14 : 0.08}
          >
            <LeafModel loading={loading} variant={variant} />
          </Float>

          <Environment preset="studio" />
        </Suspense>
      </Canvas>
    </div>
  )
}