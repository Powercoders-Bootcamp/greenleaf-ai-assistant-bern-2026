import { Environment } from '@react-three/drei'
import { Canvas } from '@react-three/fiber'
import { Bloom, EffectComposer } from '@react-three/postprocessing'
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
    <div
      className={`leaf-scene ${loading ? 'is-loading' : ''} ${isAuth ? 'is-auth' : ''}`}
    >
      <Canvas
        dpr={[1, 2]}
        gl={{ alpha: true, antialias: true }}
        shadows
        camera={{
          position: isAuth ? [0.15, 0.1, 3.25] : [0.22, 0.08, 3.15],
          fov: isAuth ? 34 : 32,
        }}
      >
        <ambientLight intensity={0.58} />

        <directionalLight
          position={[3.2, 3.4, 4.8]}
          intensity={1.75}
          castShadow
          shadow-mapSize-width={1024}
          shadow-mapSize-height={1024}
        />

        <directionalLight
          position={[-2.2, -1.6, 2.8]}
          intensity={0.45}
        />

        <pointLight
          position={[0.25, 0.8, 1.9]}
          intensity={loading ? 0.9 : 0.65}
          distance={6}
        />

        <Suspense fallback={null}>
          <LeafModel loading={loading} variant={variant} />

          <Environment preset="city" />

          <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.92, 0]} receiveShadow>
            <planeGeometry args={[5, 5]} />
            <shadowMaterial opacity={0.14} />
          </mesh>
        </Suspense>

        <EffectComposer multisampling={0}>
          <Bloom
            intensity={loading ? 0.55 : 0.32}
            luminanceThreshold={0.22}
            luminanceSmoothing={0.9}
          />
        </EffectComposer>
      </Canvas>
    </div>
  )
}