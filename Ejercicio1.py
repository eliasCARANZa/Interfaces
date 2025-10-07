import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def obtener_mascara_color(img_color, color):
    if color == 'red':
        mask = (img_color[:,:,2] > 150) & (img_color[:,:,1] < 100) & (img_color[:,:,0] < 100)
    elif color == 'green':
        mask = (img_color[:,:,1] > 150) & (img_color[:,:,2] < 100) & (img_color[:,:,0] < 100)
    elif color == 'blue':
        mask = (img_color[:,:,0] > 150) & (img_color[:,:,1] < 100) & (img_color[:,:,2] < 100)
    else:
        raise ValueError("Color debe ser 'red', 'green' o 'blue'")
    binary = np.zeros(img_color.shape[:2], dtype=np.uint8)
    binary[mask] = 1
    return binary

def marcar_centroide(img_color, cx, cy):
    img_out = img_color.copy()
    cv2.drawMarker(img_out, (cx, cy), (0,255,255), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)
    return img_out

def mostrar_comparacion(img_color, img_centroide, name):
    img_color_rgb = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
    img_centroide_rgb = cv2.cvtColor(img_centroide, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(8,4))
    plt.subplot(1,2,1)
    plt.imshow(img_color_rgb)
    plt.title(f"Original {name}")
    plt.axis('off')
    plt.subplot(1,2,2)
    plt.imshow(img_centroide_rgb)
    plt.title(f"{name} con centroide")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def figura_a(img_path):
    img_color = cv2.imread(img_path)
    binary = obtener_mascara_color(img_color, 'red')
    M = cv2.moments(binary.astype(np.uint8))
    area = int(np.sum(binary))
    ys, xs = np.where(binary > 0)
    if len(xs)>0 and len(ys)>0:
        cx_pix = int(np.mean(xs))
        cy_pix = int(np.mean(ys))
    else:
        cx_pix, cy_pix = 0, 0
    if M["m00"] != 0:
        cx_mom = int(M["m10"] / M["m00"])
        cy_mom = int(M["m01"] / M["m00"])
    else:
        cx_mom, cy_mom = 0, 0
    img_centroide = marcar_centroide(img_color, cx_mom, cy_mom)
    mostrar_comparacion(img_color, img_centroide, 'Figura a')
    print("\nFIGURA 1.a")
    print(f"a. Área (píxeles de la figura): {area}")
    print(f"b. Centroide por píxeles de figura: ({cx_pix}, {cy_pix})")
    print(f"c. Centroide por momentos (figura): ({cx_mom}, {cy_mom})")
    print(f"Momentos espaciales: m00={M['m00']}, m10={M['m10']}, m01={M['m01']}")

def figura_b(img_path):
    img_color = cv2.imread(img_path)
    binary = obtener_mascara_color(img_color, 'green')
    M = cv2.moments(binary.astype(np.uint8))
    if M["m00"] != 0:
        cx = M["m10"] / M["m00"]
        cy = M["m01"] / M["m00"]
    else:
        cx, cy = 0, 0
    ys, xs = np.where(binary > 0)
    mpq = np.sum((xs**2) * (ys**3))
    mu_pq = np.sum(((xs-cx)**2) * ((ys-cy)**3))
    gamma = ((2+3)/2)+1
    eta_pq = mu_pq / (M["m00"]**gamma) if M["m00"] != 0 else 0
    print("\nFIGURA 1.b")
    print(f"a. Momento m(2,3): {mpq}")
    print(f"b. Momento central mu(2,3): {mu_pq}")
    print(f"c. Momento central normalizado eta(2,3): {eta_pq}")

def figura_c(img_path):
    img_color = cv2.imread(img_path)
    binary = obtener_mascara_color(img_color, 'blue')
    M = cv2.moments(binary.astype(np.uint8))
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0
    huMoments = cv2.HuMoments(M)
    print("\nFIGURA 1.c")
    print(f"Centroide (figura azul): ({cx}, {cy})")
    print("a. Momentos de Hu's (Ver 2.35):")
    print(f"   i. H1: {huMoments[0][0]}")
    print(f"   ii. H2: {huMoments[1][0]}")
    print(f"   iii. H3: {huMoments[2][0]}")

def menu():
    carpeta = "imagenes"
    while True:
        print("\n--- MENÚ DE FIGURAS ---")
        print("1. Figura a (rojo)")
        print("2. Figura b (verde)")
        print("3. Figura c (azul)")
        print("4. Salir")
        opcion = input("Selecciona la figura a analizar (1-4): ")
        if opcion == '1':
            figura_a(os.path.join(carpeta, "a.png"))
        elif opcion == '2':
            figura_b(os.path.join(carpeta, "b.png"))
        elif opcion == '3':
            figura_c(os.path.join(carpeta, "c.png"))
        elif opcion == '4':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    menu()