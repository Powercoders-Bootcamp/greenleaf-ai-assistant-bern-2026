import { useGLTF } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'
import { useMemo, useRef } from 'react'
import { Box3, Group, Mesh, MeshStandardMaterial, Vector3 } from 'three'

type Props = {
  loading?: boolean
  variant?: 'default' | 'auth'
}

export default function LeafModel({
  loading = false,
  variant = 'default',
}: Props) {
  const gltf = useGLTF('/models/super_leaf_super_mario_bros.glb')
  const rootRef = useRef<Group>(null)

  const preparedScene = useMemo(() => {
    const cloned = gltf.scene.clone() as Group

    cloned.traverse((child) => {
      const mesh = child as Mesh & {
        material?: MeshStandardMaterial
      }

      if (mesh.isMesh) {
        mesh.castShadow = true
        mesh.receiveShadow = true

        if (mesh.material && 'roughness' in mesh.material) {
          mesh.material.roughness = 0.68
          mesh.material.metalness = 0.03
          mesh.material.envMapIntensity = 1.1
        }
      }
    })

    const box = new Box3().setFromObject(cloned)
    const center = box.getCenter(new Vector3())
    const size = box.getSize(new Vector3())
    const maxAxis = Math.max(size.x, size.y, size.z)

    cloned.position.sub(center)

    const targetSize = variant === 'auth' ? 1.42 : 1.55
    const scale = targetSize / maxAxis
    cloned.scale.setScalar(scale)

    const scaledBox = new Box3().setFromObject(cloned)
    const scaledCenter = scaledBox.getCenter(new Vector3())
    cloned.position.sub(scaledCenter)

    cloned.position.y += variant === 'auth' ? 0.01 : 0.02

    return cloned
  }, [gltf.scene, variant])

  useFrame((state) => {
    const group = rootRef.current
    if (!group) return

    const t = state.clock.getElapsedTime()

    if (variant === 'auth') {
      group.rotation.z = Math.sin(t * 0.9) * 0.025
      group.rotation.y = Math.sin(t * 0.65) * 0.07
      group.rotation.x = Math.cos(t * 0.8) * 0.015
      group.position.y = Math.sin(t * 1.1) * 0.012
      group.position.x = Math.cos(t * 0.6) * 0.008
      group.scale.setScalar(1)
      return
    }

    const motion = loading ? 1 : 0.55

    group.rotation.z = Math.sin(t * 1.15) * 0.05 * motion
    group.rotation.y = Math.sin(t * 0.8) * 0.14 * motion
    group.rotation.x = Math.cos(t * 0.95) * 0.035 * motion

    group.position.y = Math.sin(t * 1.4) * 0.035 * motion
    group.position.x = Math.cos(t * 0.75) * 0.02 * motion

    const scaleBase = 1
    const scalePulse = loading ? 0.035 : 0.018
    const scale = scaleBase + Math.sin(t * 1.7) * scalePulse
    group.scale.setScalar(scale)
  })

  return (
    <group ref={rootRef}>
      <primitive object={preparedScene} />
    </group>
  )
}

useGLTF.preload('/models/super_leaf_super_mario_bros.glb')