import { useGLTF } from '@react-three/drei'
import { useMemo } from 'react'
import { Box3, Group, MeshStandardMaterial, Vector3 } from 'three'

export default function LeafModel() {
  const gltf = useGLTF('/models/super_leaf_super_mario_bros.glb')

  const preparedScene = useMemo(() => {
    const cloned = gltf.scene.clone() as Group

    cloned.traverse((child) => {
      const mesh = child as Group & {
        isMesh?: boolean
        material?: MeshStandardMaterial
        castShadow?: boolean
        receiveShadow?: boolean
      }

      if (mesh.isMesh) {
        mesh.castShadow = true
        mesh.receiveShadow = true

        if (mesh.material) {
          mesh.material.roughness = 0.72
          mesh.material.metalness = 0.04
        }
      }
    })

    const box = new Box3().setFromObject(cloned)
    const center = box.getCenter(new Vector3())
    const size = box.getSize(new Vector3())
    const maxAxis = Math.max(size.x, size.y, size.z)

    cloned.position.x -= center.x
    cloned.position.y -= center.y
    cloned.position.z -= center.z

    const normalizedScale = 1.7 / maxAxis
    cloned.scale.setScalar(normalizedScale)

    return cloned
  }, [gltf.scene])

  return (
    <primitive
      object={preparedScene}
      position={[0, -0.05, 0]}
      rotation={[0, 0, 0]}
    />
  )
}

useGLTF.preload('/models/super_leaf_super_mario_bros.glb')